import json
from app.intent import detect_intent
from app.memory import get_memory, update_memory
from app.scoring import score_lead
from app.llm import generate_response
from app.rag import retrieve


def simulate_leads():

    with open("app/simulator_data.json", "r") as f:
        leads = json.load(f)

    results = []

    high, medium, low = 0, 0, 0
    converted = 0

    drop_early, drop_mid, drop_late = 0, 0, 0

    worst_cases = []

    for lead in leads:

        user_id = f"user_{lead['id']}"
        query = lead["query"]

        # Intent
        intent, _ = detect_intent(query)

        # Memory
        memory = get_memory(user_id)

        # Retrieval
        context, score = retrieve(query)

        # Generate response
        response = generate_response(context, query, memory)

        # Update memory
        update_memory(user_id, query, response, intent)

        # Lead scoring
        lead_score = score_lead(memory, intent)

        # Classification
        if lead_score == "high":
            high += 1
            converted += 1

        elif lead_score == "medium":
            medium += 1
            drop_mid += 1

        else:
            low += 1
            drop_early += 1

        # Worst case detection
        if intent == "browsing" and lead_score == "low":
            worst_cases.append({
                "query": query,
                "issue": "Vague input not progressing"
            })

        if len(worst_cases) > 3:
            worst_cases = worst_cases[:3]

        results.append({
            "user_id": user_id,
            "intent": intent,
            "lead_score": lead_score,
            "query": query,
            "response": response
        })

    # Metrics
    total = len(leads)
    conversion_rate = (converted / total) * 100

    summary = {
        "total_leads": total,
        "high_intent": high,
        "medium_intent": medium,
        "low_intent": low,
        "conversion_rate": round(conversion_rate, 2),
        "drop_early": drop_early,
        "drop_mid": drop_mid,
        "drop_late": drop_late,
        "worst_cases": worst_cases
    }

    return summary, results


if __name__ == "__main__":
    summary, results = simulate_leads()

    print("\n=== SIMULATION SUMMARY ===")
    print(json.dumps(summary, indent=2))

    print("\n=== SAMPLE RESULTS ===")
    print(json.dumps(results[:5], indent=2))