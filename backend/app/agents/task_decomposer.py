import ast

class TaskDecomposer:
    def __init__(self, llm):
        self.llm = llm

    def run(self, state):

        query = state["query"]

        prompt = f"""
Break this query into tasks with dependencies.

Return a Python list of dicts:
[
  {{"id": 1, "task": "...", "depends_on": []}}
]

Example:
React vs Next.js:
[
 {{"id": 1, "task": "Understand React", "depends_on": []}},
 {{"id": 2, "task": "Understand Next.js", "depends_on": []}},
 {{"id": 3, "task": "Compare", "depends_on": [1,2]}},
 {{"id": 4, "task": "Recommend", "depends_on": [3]}}
]
"""

        response = self.llm.invoke(prompt).content

        try:
            tasks = ast.literal_eval(response)
        except:
            tasks = [{"id": 1, "task": query, "depends_on": []}]

        state["tasks"] = tasks
        state["completed_tasks"] = []

        return state