from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

INTENTS = {
    "buy": ["buy house", "purchase property", "own house"],
    "rent": ["rent house", "rental property", "lease flat"],
    "investment": ["investment property", "roi property", "invest in real estate"],
    "browsing": ["just looking", "exploring", "checking options"]
}

intent_embeddings = {
    intent: model.encode(phrases)
    for intent, phrases in INTENTS.items()
}


def detect_intent(query):
    query_embedding = model.encode(query)

    best_intent = None
    best_score = -1

    for intent, embeddings in intent_embeddings.items():
        score = util.cos_sim(query_embedding, embeddings).max().item()

        if score > best_score:
            best_score = score
            best_intent = intent

    return best_intent, best_score