from fastapi import FastAPI
from pydantic import BaseModel
import os
from app.core.state import create_initial_state
from langchain_openai import ChatOpenAI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.graph.decision_graph import build_graph
from app.agents.generator import FinalGenerator
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://decide-dsobuji1g-ankits-projects-a53425ee.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize graph once
llm = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0
)
graph = build_graph(llm)
generator = FinalGenerator(llm)

class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def stream_llm_response(query: QueryRequest):

    state = create_initial_state(query)

    result = graph.invoke(state)

    # Step 2: stream ONLY final generation
    async for token in generator.stream(result):
        yield token



@app.post("/query-stream")
async def query_stream(request: QueryRequest):
    return StreamingResponse(
        stream_llm_response(request.query),
        media_type="text/plain"
    )