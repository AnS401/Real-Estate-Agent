# app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
import uuid

# Core modules
from app.memory import get_memory, update_memory
from app.intent_semantic import decide_intent
from app.rag import retrieve
from app.llm import generate_response

# Intelligence layers
from app.repetition_utils import is_repetitive, diversify_response
from app.dropoff_utils import detect_dropoff
from app.conversion_utils import compute_conversion_probability
from app.cta_utils import should_show_cta, get_cta_text
from app.human_override import should_escalate_to_human, get_human_message

# Optional logging
from app.logger import log_interaction


app = FastAPI()

SIMILARITY_THRESHOLD = 3.0


class Query(BaseModel):
    query: str
    user_id: str = None


@app.post("/chat")
def chat(q: Query):

    # --- USER SETUP ---
    user_id = q.user_id or str(uuid.uuid4())
    query = q.query

    # --- MEMORY ---
    memory = get_memory(user_id)

    # --- INTENT (HIGH / LOW using semantic + context) ---
    intent = decide_intent(query, memory)

    # --- RAG RETRIEVAL ---
    context, score = retrieve(query)

    # --- RESPONSE GENERATION ---
    if score > SIMILARITY_THRESHOLD:
        response = "Could you clarify your requirement a bit? I’ll guide you better."
        source = "fallback"
    else:
        response = generate_response(context, query, memory)
        source = "rag_llm"

    # --- REPETITION CONTROL ---
    if is_repetitive(response, memory):
        response = diversify_response(response)

    # --- DROP-OFF DETECTION ---
    dropoff = detect_dropoff(query, memory)

    # --- CONVERSION PROBABILITY ---
    conversion_prob = compute_conversion_probability(memory)

    # --- CTA CONTROL ---
    cta_used = False
    turn_count = len(memory.get("queries", []))

    if should_show_cta(intent, conversion_prob, dropoff, memory):
        response += get_cta_text(turn_count)
        cta_used = True

    # --- HUMAN OVERRIDE ---
    escalate, reason = should_escalate_to_human(
        query,
        intent,
        conversion_prob,
        dropoff,
        memory
    )

    if escalate:
        response += get_human_message(reason)

    # --- MEMORY UPDATE ---
    update_memory(user_id, query, response, intent, cta_used)

    # --- LOGGING ---
    try:
        log_interaction(
            user_id=user_id,
            query=query,
            response=response,
            intent=intent,
            conversion_probability=conversion_prob,
            dropoff=dropoff,
            escalated=escalate
        )
    except:
        pass  # prevent crash if logger not configured

    # --- FINAL RESPONSE ---
    return {
        "user_id": user_id,
        "intent": intent,
        "conversion_probability": conversion_prob,
        "dropoff": dropoff,
        "escalated": escalate,
        "response": response,
        "source": source,
        "similarity_score": float(score)
    }