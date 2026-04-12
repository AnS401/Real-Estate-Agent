import re

def score_lead(memory, intent=None):

    if not memory:
        return "low"

    intent = (intent or "").lower()

    texts = []
    for m in memory:
        if isinstance(m, dict):
            texts.append(m.get("query", ""))
        else:
            texts.append(str(m))

    combined_text = " ".join(texts).lower()
    length = len(memory)

    score = 0

    #  STRONG SIGNALS

    # buy / rent intent
    if any(word in combined_text for word in ["buy", "purchase","looking", "rent", "need", "require", "interested", "want", "ready", "budget", "urgent"]):
        score += 2

    # action signals
    if any(word in combined_text for word in ["visit", "book", "schedule", "contact", "ready", "urgent"]):
        score += 3

    #  BUDGET DETECTION (CRITICAL FIX)
    if re.search(r"\d+\s?(k|l|lac|lakh|cr|crore)", combined_text):
        score += 3

    # explicit budget words
    if any(word in combined_text for word in ["budget", "price", "cost", "range", "under"]):
        score += 2

    #  MEDIUM SIGNALS
    if any(word in combined_text for word in ["looking", "explore", "options", "compare", "check"]):
        score += 1

    if any(word in combined_text for word in ["investment"]):
        score += 1

    #  intent boost
    if "buy" in intent or "rent" in intent:
        score += 1

    #  engagement bonus
    if length >= 3:
        score += 1

    #  FINAL DECISION
    if score >= 5:
        return "high"
    elif score >= 2:
        return "medium"
    else:
        return "low"