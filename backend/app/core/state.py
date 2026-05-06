from typing import TypedDict, List, Dict, Optional


class AgentState(TypedDict):
    # Input
    query: str

    # Task system
    tasks: List[str]
    current_task_index: int

    # Agent routing
    active_agents: List[str]

    # Outputs from agents
    research_docs: List[str]
    comparison: Optional[str]
    reasoning: Optional[str]

    # Final output
    final_answer: Optional[str]

    # Evaluation
    confidence: float
    retry_count: int
    max_retries: int

    # Research
    research_docs: List[str]
    research_trace: List[str]

    #Comparison
    comparison: str

    #Reasoning
    reasoning: str

    #Aggregator
    combined_output: str

    #Decomposer
    tasks: list
    current_task_index: int

    #Supervisor
    next_agent: str

    history: list



def create_initial_state(query: str) -> AgentState:
    return {
        "query": query,

        "tasks": [],
        "current_task_index": 0,

        "active_agents": [],

        "research_docs": [],
        "comparison": None,
        "reasoning": None,

        "final_answer": None,

        "confidence": 0.0,
        "retry_count": 0,
        "max_retries": 2,

        "research_docs": [],
        "research_trace": [],

        "comparison":"",

        "reasoning": "",

        "combined_output": "",

        "tasks": [],
        "current_task_index": 0,

        "next_agent": "",

        "history": [],
    }