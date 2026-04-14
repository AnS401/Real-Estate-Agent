# app/human_override.py

HUMAN_TRIGGER_KEYWORDS = [
    "talk to agent",
    "connect me",
    "call me",
    "human",
    "support person",
    "representative"
]

CONFUSION_KEYWORDS = [
    "not understanding",
    "confusing",
    "doesn't make sense",
    "what do you mean",
    "explain again"
]


def should_escalate_to_human(query, intent, conversion_prob, dropoff, memory):
    q = query.lower()

    # --- RULE 1: User explicitly asks ---
    if any(k in q for k in HUMAN_TRIGGER_KEYWORDS):
        return True, "user_requested"

    # --- RULE 2: Confusion signals ---
    if any(k in q for k in CONFUSION_KEYWORDS):
        return True, "user_confused"

    # --- RULE 3: High intent + strong conversion ---
    if intent == "high" and conversion_prob > 0.8:
        return True, "ready_to_convert"

    # --- RULE 4: Repeated drop-off ---
    drop_count = memory.get("dropoff_count", 0)
    if dropoff:
        drop_count += 1
        memory["dropoff_count"] = drop_count

        if drop_count >= 2:
            return True, "repeated_dropoff"

    return False, None


def get_human_message(reason):
    messages = {
        "user_requested": "I’ll connect you with one of our experts right away.",
        "user_confused": "Let me connect you with a specialist who can explain this better.",
        "ready_to_convert": "This looks like a good fit. I can connect you with our expert to help you finalize.",
        "repeated_dropoff": "I think a quick chat with our expert would help you better. Want me to connect you?"
    }

    return messages.get(reason, "Let me connect you with our team for better assistance.")