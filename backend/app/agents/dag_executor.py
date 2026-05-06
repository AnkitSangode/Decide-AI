import asyncio
from app.graph.utils import get_ready_tasks


class DAGExecutor:
    def __init__(self, router, agents):
        self.router = router
        self.agents = agents

    def run(self, state):

        ready_tasks = get_ready_tasks(state)

        if not ready_tasks:
            return state

        for task in ready_tasks:

            temp_state = state.copy()
            temp_state["current_task"] = task["task"]

            # 🔁 Tool routing
            temp_state = self.router.run(temp_state)
            tools = temp_state.get("next_agent", [])

            # 🔁 Execute tools (sequential for now)
            for tool in tools:
                if tool in self.agents:
                    temp_state = self.agents[tool].run(temp_state)

            # ✅ Mark task complete
            state["completed_tasks"].append(task["id"])

            # 🔁 Merge results
            for key, val in temp_state.items():
                if key not in state or not state[key]:
                    state[key] = val

        return state