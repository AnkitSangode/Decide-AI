from langchain_openai import ChatOpenAI

class FinalGenerator:
    def __init__(self, llm):
        self.llm = llm

    def build_prompt(self, state):
        query = state["query"]
        combined = state.get("combined_output", "")

        return f"""
You are a decision-making AI system.

User Query:
{query}

Information:
{combined}


Instructions:
- Provide a clear and confident recommendation
- Do NOT stay neutral
- Choose ONE best option unless absolutely necessary
- Tailor recommendation to real-world scenarios (freelancing, startups, production apps)
- Justify your decision

Format:


🔹 Summary  
🔹 Comparison  
🔹 Recommendation (decisive)  
🔹 Trade-offs  
🔹 Final Verdict  
🔹 Confidence  
"""

    # 🔥 STREAM TOKENS
    async def stream(self, state):
        prompt = self.build_prompt(state)

        async for chunk in self.llm.astream(prompt):
            if chunk.content:
                yield chunk.content