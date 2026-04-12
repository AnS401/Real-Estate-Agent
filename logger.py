import json
from datetime import datetime

LOG_FILE = "leads.json"


def log_interaction(user_id, query, response, intent, score):
    log_entry = {
        "user_id": user_id,
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "response": response,
        "intent": intent,
        "intent_score": score
    }

    try:
        try:
            with open(LOG_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(log_entry)

        with open(LOG_FILE, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print("LOG ERROR:", e)