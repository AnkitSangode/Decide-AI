class SupervisorAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, state):

        tasks = state.get("tasks", [])
        index = state.get("current_task_index", 0)

        # =========================
        # STOP CONDITION
        # =========================
        if index >= len(tasks):
            state["next_agent"] = "done"
            return state

        current_task = tasks[index]

        # =========================
        # 🧠 DECIDE AGENT
        # =========================
        prompt = f"""
You are a supervisor agent.

Task:
{current_task}

Decide which agent should handle this task.

Available agents:
- research
- comparison
- reasoning

Rules:
- research → for gathering information
- comparison → for comparing options
- reasoning → for final decision

Return ONLY one word:
research OR comparison OR reasoning
"""

        decision = self.llm.invoke(prompt).content.lower().strip()

        # fallback safety
        if decision not in ["research", "comparison", "reasoning"]:
            decision = "research"

        # =========================
        # SAVE DECISION
        # =========================
        state["next_agent"] = decision

        return state