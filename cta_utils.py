# app/cta_utils.py

def should_show_cta(intent, conversion_prob, dropoff, session_memory):
    history = session_memory.get("cta_history", [])
    turn_count = len(session_memory.get("queries", []))

    # --- RULE 1: Must be high intent ---
    if intent != "high":
        return False

    # --- RULE 2: Strong conversion probability ---
    if conversion_prob < 0.65:
        return False

    # --- RULE 3: No drop-off ---
    if dropoff:
        return False

    # --- RULE 4: Avoid early CTA ---
    if turn_count < 3:
        return False

    # --- RULE 5: Avoid repetition ---
    if history:
        if history[-1] is True:
            return False

    return True


def get_cta_text(turn_count):
    """
    Adaptive CTA based on conversation maturity
    """

    # Softer CTA for early high-intent users
    if turn_count < 5:
        return "If you'd like, I can help you explore this further."

    # Stronger CTA for mature conversations
    return "I can help arrange a site visit or connect you with our expert."