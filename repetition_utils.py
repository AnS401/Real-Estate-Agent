from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def is_repetitive(new_response, session_memory):
    past_responses = session_memory.get("responses", [])

    if not past_responses:
        return False

    new_emb = model.encode([new_response])

    for past in past_responses[-3:]:
        past_emb = model.encode([past])
        sim = cosine_similarity(new_emb, past_emb)[0][0]

        if sim > 0.85:
            return True

    return False


def diversify_response(response):
    variations = [
        response.replace("great option", "solid choice"),
        response.replace("you can find", "you may explore"),
        response.replace("options", "properties")
    ]

    return variations[0]