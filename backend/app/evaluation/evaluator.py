class Evaluator:
    def __init__(self, llm):
        self.llm = llm

    def run(self, state):

        query = state["query"]
        reasoning = state.get("reasoning", "")

        if not reasoning:
            state["confidence"] = 0.0
            return state

        prompt = f"""
You are an evaluator.

User Query:
{query}

Generated Answer:
{reasoning}

Evaluate the quality of this answer.

Return ONLY a number between 0 and 1:
0 = completely wrong
1 = perfect answer
"""

        score = self.llm.invoke(prompt).content.strip()

        try:
            confidence = float(score)
        except:
            confidence = 0.5

        state["confidence"] = confidence

        return state