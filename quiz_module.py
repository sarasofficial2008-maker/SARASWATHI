from gemini_client import call_gemini


def generate_quiz(text: str) -> str:
    prompt = (
        "Create a short quiz based on the following topic or content. "
        "Return it in a clear format with 5 questions, each with 4 options and the correct answer.\n\n"
        f"Content: {text}"
    )
    return call_gemini(prompt)
