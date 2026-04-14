def compute_conversion_probability(session_memory):
    history = session_memory.get("intent_history", [])
    queries = session_memory.get("queries", [])

    if not history:
        return 0.0

    high_count = history.count("high")
    total_turns = len(history)

    consistency = high_count / total_turns

    recent_boost = 1 if history[-2:] == ["high", "high"] else 0

    urgency_keywords = ["urgent", "finalize", "ready", "book", "visit"]

    urgency_flag = any(
        any(k in q.lower() for k in urgency_keywords)
        for q in queries[-3:]
    )

    score = (
        0.5 * consistency +
        0.3 * recent_boost +
        0.2 * int(urgency_flag)
    )

    return round(min(score, 1.0), 2)