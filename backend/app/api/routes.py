from fastapi import APIRouter
from langchain_openai import ChatOpenAI
from app.core.state import create_initial_state
from app.graph.decision_graph import build_graph
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

llm = ChatOpenAI(model="gpt-4o-mini")

graph = build_graph(llm)
    

@router.post("/query")
def query_ai(query: str):

    state = create_initial_state(query)

    result = graph.invoke(state)

    return {
        "query": query,
        "answer": result["final_answer"]
    }