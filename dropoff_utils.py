DROP_SIGNALS = [
    "not sure", "maybe later", "just checking",
    "no hurry", "leave it", "will see"
]

def detect_dropoff(query, session_memory):
    q = query.lower()

    if any(k in q for k in DROP_SIGNALS):
        return True

    history = session_memory.get("intent_history", [])

    if len(history) >= 2:
        if history[-2] == "high" and history[-1] == "low":
            return True

    return False