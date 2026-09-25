from gemini_client import call_gemini


def answer_question(question: str) -> str:
    prompt = (
        "Answer the following question clearly and accurately. "
        "If the question is ambiguous, explain the likely interpretation.\n\n"
        f"Question: {question}"
    )
    return call_gemini(prompt)
