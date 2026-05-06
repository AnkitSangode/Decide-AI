import asyncio


class ParallelResearchAgent:
    def __init__(self, rag_tool):
        self.rag_tool = rag_tool

    async def _run_single(self, query):
        return self.rag_tool.run(query)

    async def run(self, state):

        tasks = state.get("tasks", [])
        index = state.get("current_task_index", 0)

        # Select only "understand" tasks
        parallel_tasks = [
            t for t in tasks[index:]
            if "understand" in t.lower()
        ]

        if not parallel_tasks:
            return state

        # Run in parallel
        results = await asyncio.gather(*[
            self._run_single(task) for task in parallel_tasks
        ])

        # Flatten results
        docs = []
        for r in results:
            docs.extend(r)

        state["research_docs"] = docs

        # Move index forward by number of tasks completed
        state["current_task_index"] += len(parallel_tasks)

        return state