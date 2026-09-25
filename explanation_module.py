from gemini_client import call_gemini


def explain_concept(text: str) -> str:
    prompt = (
        "Explain this concept in a simple, engaging, and student-friendly way. "
        "Use plain language, examples, and a clear structure.\n\n"
        f"Concept: {text}"
    )
    return call_gemini(prompt)
