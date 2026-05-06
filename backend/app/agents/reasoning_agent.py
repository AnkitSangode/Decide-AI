class ReasoningAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, state):

        query = state["query"]
        comparison = state.get("comparison", "")

        if not comparison:
            state["reasoning"] = "Not enough information to make a decision."
            return state

        # =========================
        # 🧠 PROMPT
        # =========================
        prompt = f"""
You are an expert decision-making assistant.

User Query:
{query}

Comparison Data:
{comparison}

Your task:
1. Recommend the best option
2. Explain WHY it is the best
3. Mention trade-offs
4. Keep it clear and structured

Output format:

Recommendation:
...

Reason:
- point
- point

Trade-offs:
- point
- point
"""

        response = self.llm.invoke(prompt).content

        # =========================
        # SAVE TO STATE
        # =========================
        state["reasoning"] = response

        return state