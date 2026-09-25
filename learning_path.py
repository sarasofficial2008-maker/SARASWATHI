from gemini_client import call_gemini


def get_learning_recommendations(text: str) -> str:
    prompt = (
        "Create a practical learning path for the topic below. Include: "
        "1) starter concepts, 2) key skills to build, 3) practice activities, "
        "and 4) a recommended order of study. Make it motivating and structured.\n\n"
        f"Topic: {text}"
    )
    return call_gemini(prompt)
