# from app.tools.rag_tool import RAGTool

# rag = RAGTool()

# docs = rag.run("React vs Next.js")

# print(docs)



# from app.agents.research_agent import ResearchAgent
# from app.core.state import create_initial_state
# from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(model="gpt-4o-mini")

# agent = ResearchAgent(llm)

# state = create_initial_state("React vs Next.js")

# result = agent.run(state)

# print(result["research_docs"])
# print("\nTRACE:\n")
# for t in result["research_trace"]:
#     print(t)




# from app.agents.comparison_agent import ComparisonAgent
# from app.core.state import create_initial_state
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv

# load_dotenv()


# llm = ChatOpenAI(model="gpt-4o-mini")

# agent = ComparisonAgent(llm)

# state = create_initial_state("React vs Next.js")

# state["research_docs"] = [
#     "React is flexible and has a large ecosystem.",
#     "Next.js provides server-side rendering and is SEO friendly."
# ]

# result = agent.run(state)

# print(result["comparison"])



# from app.agents.reasoning_agent import ReasoningAgent
# from app.core.state import create_initial_state
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv

# load_dotenv()

# llm = ChatOpenAI(model="gpt-4o-mini")

# agent = ReasoningAgent(llm)

# state = create_initial_state("React vs Next.js for freelancing")

# state["comparison"] = """
# React:
# - Flexible
# - Large ecosystem

# Next.js:
# - SEO friendly
# - Production ready
# """

# result = agent.run(state)

# print(result["reasoning"])



# from app.agents.task_decomposer import TaskDecomposer
# from app.core.state import create_initial_state
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv

# load_dotenv()

# llm = ChatOpenAI(model="gpt-4o-mini")

# agent = TaskDecomposer(llm)

# state = create_initial_state("React vs Next.js for freelancing")

# result = agent.run(state)

# print(result["tasks"])




from app.agents.supervisor_agent import SupervisorAgent
from app.core.state import create_initial_state
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

agent = SupervisorAgent(llm)

state = create_initial_state("React vs Next.js")

state["tasks"] = [
    "Understand React",
    "Compare both",
    "Recommend best option"
]

result = agent.run(state)

print(result["next_agent"])