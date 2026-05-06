class ComparisonAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, state):

        docs = state.get("research_docs", [])

        if not docs:
            state["comparison"] = "No data available for comparison."
            return state

        # =========================
        # 🧠 PROMPT
        # =========================
        prompt = f"""
You are a comparison expert.

Based on the following information:

{docs}

Do the following:
1. Identify the main options being discussed
2. Compare them clearly
3. Use bullet points
4. Keep it structured and easy to read

Output format:

Option 1:
- point
- point

Option 2:
- point
- point
"""

        response = self.llm.invoke(prompt).content

        # =========================
        # SAVE TO STATE
        # =========================
        state["comparison"] = response

        return state