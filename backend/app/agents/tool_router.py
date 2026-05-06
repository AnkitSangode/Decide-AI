import json

class ToolRouter:
    def __init__(self, llm):
        self.llm = llm

        self.tools = {
            "research": "Use for understanding concepts and gathering information",
            "comparison": "Use for comparing multiple options",
            "reasoning": "Use for making decisions and recommendations"
        }

    def run(self, state):

        tasks = state.get("tasks", [])
        index = state.get("current_task_index", 0)

        # STOP
        if index >= len(tasks):
            state["next_agent"] = ["done"]
            return state

        current_task = tasks[index]

        tool_descriptions = "\n".join(
            [f"{k}: {v}" for k, v in self.tools.items()]
        )

        prompt = f"""
You are an intelligent tool router.

Task:
{current_task}

Available tools:
{tool_descriptions}

Rules:
- If task involves comparison → include "comparison"
- If task involves decision, recommendation, or "better" → include "reasoning"
- A task can require MULTIPLE tools

Return a Python list of tools.

Examples:
"What is better React or Next.js"
→ ["comparison", "reasoning"]

"Compare React and Next.js"
→ ["comparison"]

"Explain React"
→ ["research"]
"""

        response = self.llm.invoke(prompt).content

        
        try:
            tool_scores = json.loads(response)
        except:
            tool_scores = [{"tool": "research", "score": 1.0}]


        state["tool_scores"] = tool_scores

        return state