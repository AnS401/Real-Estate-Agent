memory_store = {}


def get_memory(user_id):
    return memory_store.get(user_id, [])


def update_memory(user_id, query, response, intent):
    if user_id not in memory_store:
        memory_store[user_id] = []

    memory_store[user_id].append({
        "query": query,
        "response": response,
        "intent": intent
    })

    # keep last 10
    memory_store[user_id] = memory_store[user_id][-10:]