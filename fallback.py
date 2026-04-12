def fallback_response(mode="clarify"):

    if mode == "clarify":
        return {
            "response": "Could you share a bit more detail? For example, budget or location."
        }

    elif mode == "human":
        return {
            "response": "I want to give you accurate guidance. You can contact our expert at +91 9876543210."
        }

    return {"response": "Let me help you with that."}