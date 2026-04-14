# app/memory.py

memory_store = {}


def get_memory(user_id):
    return memory_store.setdefault(user_id, {
        "queries": [],
        "responses": [],
        "intent_history": [],
        "cta_history": [],       # ✅ NEW
        "dropoff_count": 0       # ✅ NEW
    })


def update_memory(user_id, query, response, intent, cta_used):
    memory = get_memory(user_id)

    memory["queries"].append(query)
    memory["responses"].append(response)
    memory["intent_history"].append(intent)
    memory["cta_history"].append(cta_used)

    # keep last 10 entries
    memory["queries"] = memory["queries"][-10:]
    memory["responses"] = memory["responses"][-10:]
    memory["intent_history"] = memory["intent_history"][-10:]
    memory["cta_history"] = memory["cta_history"][-10:]