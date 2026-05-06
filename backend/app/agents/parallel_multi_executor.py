import asyncio


class ParallelMultiToolExecutor:
    def __init__(self, agents):
        self.agents = agents

    async def _run_single(self, agent, state):
        return agent.run(state)

    async def run(self, state):

        selected_tools = state.get("next_agent", [])

        if not selected_tools:
            return state

        # Create async tasks
        tasks = []
        for tool in selected_tools:
            if tool in self.agents:
                tasks.append(
                    self._run_single(self.agents[tool], state.copy())
                )

        # Run all tools in parallel
        results = await asyncio.gather(*tasks)

        # Merge results
        for result in results:
            for key, value in result.items():
                if key not in state or not state[key]:
                    state[key] = value

        return state