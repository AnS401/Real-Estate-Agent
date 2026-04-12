import json
import os
from datetime import datetime

LOG_FILE = "data/leads.json"


def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_logs(data):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def log_interaction(user_id, query, response, intent, score=None):
    logs = load_logs()

    entry = {
        "user_id": user_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "response": response,
        "intent": intent,
        "intent_confidence": score
    }

    logs.append(entry)

    save_logs(logs)