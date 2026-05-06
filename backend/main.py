from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from app.core.state import create_initial_state
from app.graph.decision_graph import build_graph
from app.agents.generator import FinalGenerator

load_dotenv()

app = FastAPI()

# ---------------- CORS ---------------- #

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://decide-ai-nine.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Health Routes ---------------- #

@app.get("/")
async def root():
    return {"message": "Decide AI Backend Running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Explicit OPTIONS handler for streaming endpoint
@app.options("/query-stream")
async def options_query_stream():
    return JSONResponse(content={"message": "OK"})

# ---------------- AI Initialization ---------------- #

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

graph = build_graph(llm)
generator = FinalGenerator(llm)

# ---------------- Request Schema ---------------- #

class QueryRequest(BaseModel):
    query: str

# ---------------- Helper Function ---------------- #

async def generate_stream(query: str):

    state = create_initial_state(query)

    result = graph.invoke(state)

    async for token in generator.stream(result):
        yield token

# ---------------- Routes ---------------- #

@app.post("/query-stream")
async def query_stream(request: QueryRequest):

    return StreamingResponse(
        generate_stream(request.query),
        media_type="text/plain"
    )