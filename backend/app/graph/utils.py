def get_ready_tasks(state):

    tasks = state["tasks"]
    completed = state.get("completed_tasks", [])

    ready = []

    for t in tasks:
        if t["id"] in completed:
            continue

        if all(dep in completed for dep in t["depends_on"]):
            ready.append(t)

    return ready