class MultiToolExecutor:
    def __init__(self, agents):
        self.agents = agents

    def run(self, state):

        selected_tools = state.get("next_agent", [])

        for tool in selected_tools:
            if tool in self.agents:
                state = self.agents[tool].run(state)

        return state