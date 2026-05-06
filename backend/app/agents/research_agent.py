from app.tools.rag_tool import RAGTool


class ResearchAgent:
    def __init__(self, llm):
        self.llm = llm
        self.rag_tool = RAGTool()

    def run(self, state):

        query = state["query"]
        trace = []

        final_docs = []

        # 🔁 ReAct Loop
        for step in range(2):

            # =========================
            # 🧠 THOUGHT
            # =========================
            thought_prompt = f"""
You are a research agent.

Query: {query}

Rules:
- You MUST prefer retrieving external knowledge
- Only skip retrieval if the query is extremely trivial (like greetings)

Should you retrieve external knowledge?

Answer ONLY YES or NO.
"""

            thought = self.llm.invoke(thought_prompt).content
            trace.append(f"Thought {step+1}: {thought}")

            if "no" in thought.lower():
                break

            # =========================
            # ⚙️ ACTION (RAG)
            # =========================
            docs = self.rag_tool.run(query, k=3)

            trace.append(f"Action {step+1}: Retrieved {len(docs)} documents")

            # =========================
            # 👀 OBSERVATION
            # =========================
            observation_prompt = f"""
We retrieved the following information:

{docs}

Is this enough to answer the query properly?

Answer YES or NO.
"""

            observation = self.llm.invoke(observation_prompt).content
            trace.append(f"Observation {step+1}: {observation}")

            final_docs = docs

            if "yes" in observation.lower():
                break

        # fallback
        if not final_docs:
            final_docs = docs if 'docs' in locals() else []

        # =========================
        # SAVE TO STATE
        # =========================
        state["research_docs"] = final_docs
        state["research_trace"] = trace

        return state