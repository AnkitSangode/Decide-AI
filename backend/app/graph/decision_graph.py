from langgraph.graph import StateGraph, END
from typing import Dict

# Agents
from app.agents.task_decomposer import TaskDecomposer
from app.agents.tool_router import ToolRouter
from app.agents.research_agent import ResearchAgent
from app.agents.comparison_agent import ComparisonAgent
from app.agents.reasoning_agent import ReasoningAgent
from app.agents.aggregator import AggregatorAgent
from app.agents.dag_executor import DAGExecutor
from app.graph.conditions import route_after_evaluation

# Evaluator
from app.evaluation.evaluator import Evaluator


# =========================
# 🧠 BUILD GRAPH
# =========================
def build_graph(llm):

    # =========================
    # AGENTS
    # =========================
    decomposer = TaskDecomposer(llm)
    router = ToolRouter(llm)

    research = ResearchAgent(llm)
    comparison = ComparisonAgent(llm)
    reasoning = ReasoningAgent(llm)

    evaluator = Evaluator(llm)
    aggregator = AggregatorAgent()

    # DAG Executor (core brain)
    dag_executor = DAGExecutor(
        router=router,
        agents={
            "research": research,
            "comparison": comparison,
            "reasoning": reasoning
        }
    )

    # =========================
    # GRAPH INIT
    # =========================
    graph = StateGraph(Dict)

    # =========================
    # NODES
    # =========================
    graph.add_node("decomposer", decomposer.run)
    graph.add_node("executor", dag_executor.run)
    graph.add_node("evaluator", evaluator.run)
    graph.add_node("aggregator", aggregator.run)

    # =========================
    # ENTRY POINT
    # =========================
    graph.set_entry_point("decomposer")

    # =========================
    # FLOW
    # =========================
    graph.add_edge("decomposer", "executor")

    # Execution loop
    graph.add_edge("executor", "evaluator")

    # Conditional routing after evaluation
    graph.add_conditional_edges(
        "evaluator",
        route_after_evaluation,
        {
            "replan": "decomposer",   # 🔁 retry with new plan
            "continue": "executor",   # 🔁 continue DAG execution
            "done": "aggregator"      # ✅ finish
        }
    )

    # Final step (NO generator here)
    graph.add_edge("aggregator", END)

    return graph.compile()