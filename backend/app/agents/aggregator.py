class AggregatorAgent:
    def run(self, state):

        research = state.get("research_docs", [])
        comparison = state.get("comparison", "")
        reasoning = state.get("reasoning", "")

        # Combine everything
        combined = f"""
Research Data:
{research}

Comparison:
{comparison}

Reasoning:
{reasoning}
"""

        state["combined_output"] = combined

        return state