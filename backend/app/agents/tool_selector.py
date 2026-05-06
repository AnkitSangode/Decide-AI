class ToolSelector:
    def run(self, state):

        tool_scores = state.get("tool_scores", [])

        # sort by confidence
        tool_scores = sorted(
            tool_scores,
            key=lambda x: x["score"],
            reverse=True
        )

        # pick top tools
        selected = [
            t["tool"] for t in tool_scores if t["score"] > 0.6
        ]

        if not selected:
            selected = [tool_scores[0]["tool"]]

        state["next_agent"] = selected

        return state