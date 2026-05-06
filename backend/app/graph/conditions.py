def route_agent(state):
    return state.get("next_agent", ["done"])


def increment_index(state):
    state["current_task_index"] += 1
    return state


def route_after_evaluation(state):

    confidence = state.get("confidence", 0.0)
    retries = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 2)

    total_tasks = len(state.get("tasks", []))
    completed = len(state.get("completed_tasks", []))

    # ✅ All tasks done
    if completed >= total_tasks:
        return "done"

    # ❌ Low confidence → retry
    if confidence < 0.6:
        if retries < max_retries:
            state["retry_count"] += 1
            return "replan"
        else:
            return "continue"

    # ✅ Good result → continue
    state["retry_count"] = 0
    return "continue"