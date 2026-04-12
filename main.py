from fastapi import FastAPI
from pydantic import BaseModel
import uuid

from app.rag import retrieve
from app.intent import detect_intent
from app.memory import get_memory, update_memory
from app.scoring import score_lead
from app.llm import generate_response
from app.fallback import fallback_response
from app.logger import log_interaction

app = FastAPI()

SIMILARITY_THRESHOLD = 3.0


class Query(BaseModel):
    query: str
    user_id: str = None


@app.post("/chat")
def chat(q: Query):
    user_id = q.user_id or str(uuid.uuid4())
    query = q.query

    # 🔹 Intent Detection (SAFE)
    try:
        result = detect_intent(query)
        if isinstance(result, tuple):
            intent, intent_score = result
        else:
            intent = result
            intent_score = 0.0
    except:
        intent = "unknown"
        intent_score = 0.0

    # 🔹 Memory
    memory = get_memory(user_id)

    # 🔥 CLEAN MEMORY (IMPORTANT)
    memory = [m for m in memory if isinstance(m, dict)]

    # 🔹 Retrieval
    context, similarity_score = retrieve(query)

    print("\n--- DEBUG ---")
    print("Intent:", intent)
    print("Score:", intent_score)
    print("Similarity:", similarity_score)
    print("Memory:", memory)
    print("----------------\n")

    # 🔹 Response Generation
    if similarity_score > SIMILARITY_THRESHOLD:
        response = fallback_response("clarify")["response"]
        source = "fallback_clarify"
    else:
        try:
            response = generate_response(context, query, memory)
            if not response:
                raise Exception("Empty LLM response")
            source = "rag_llm"
        except:
            if context:
                response = "I found some options — want me to refine them?"
                source = "context_fallback"
            else:
                response = fallback_response("human")["response"]
                source = "fallback_human"

    # 🔹 Lead Scoring
    lead_score = score_lead(memory, intent)

    # 🔹 Conversion Logic
    if lead_score == "high":
        if "contact" not in response.lower():
            response += "Want me to arrange a visit or connect you with our expert?"

    elif lead_score == "medium":
        response += "I can narrow down options further if you'd like."

    # 🔹 Update Memory
    update_memory(user_id, query, response, intent)

    # 🔹 Logging
    log_interaction(user_id, query, response, intent, intent_score)

    return {
        "user_id": user_id,
        "intent": intent,
        "intent_score": float(intent_score),
        "response": response,
        "lead_score": lead_score,
        "source": source,
        "similarity_score": float(similarity_score)
    }