class MemoryManager:
    def __init__(self):
        pass

    # =========================
    # READ MEMORY
    # =========================
    def read(self, state):

        history = state.get("history", [])

        formatted = ""
        for item in history:
            formatted += f"User: {item['query']}\n"
            formatted += f"AI: {item['answer']}\n\n"

        return formatted

    # =========================
    # WRITE MEMORY
    # =========================
    def write(self, state):

        history = state.get("history", [])

        history.append({
            "query": state["query"],
            "answer": state.get("final_answer", "")
        })

        state["history"] = history

        return state