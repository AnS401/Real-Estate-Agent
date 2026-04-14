from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

INTENT_ANCHORS = {
    "low": [
        "just exploring options",
        "not sure yet",
        "casually browsing",
        "no urgency",
        "checking options"
    ],
    "high": [
        "ready to buy property",
        "want to schedule site visit",
        "finalizing property",
        "need property urgently",
        "book a visit"
    ]
}

anchor_embeddings = {
    label: model.encode(sentences)
    for label, sentences in INTENT_ANCHORS.items()
}


def semantic_intent_score(query: str):
    query_emb = model.encode([query])

    scores = {}
    for label, emb_list in anchor_embeddings.items():
        sim = cosine_similarity(query_emb, emb_list).max()
        scores[label] = sim

    return scores


def decide_intent(query, session_memory):
    scores = semantic_intent_score(query)

    low_score = scores["low"]
    high_score = scores["high"]

    q = query.lower()

    # HARD RULES
    if any(k in q for k in ["book", "visit", "schedule", "finalize", "ready", "urgent"]):
        final_intent = "high"

    elif any(k in q for k in ["just", "exploring", "not sure", "maybe", "checking"]):
        final_intent = "low"

    else:
        final_intent = "high" if high_score > low_score else "low"

    # CONTEXT BOOST
    history = session_memory.get("intent_history", [])

    if history:
        prev = history[-1]

        if prev == "high" and final_intent == "low":
            if any(k in q for k in ["price", "options", "location", "bhk"]):
                final_intent = "high"

    session_memory.setdefault("intent_history", []).append(final_intent)

    return final_intent