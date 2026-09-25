from gemini_client import call_gemini


def summarize_text(text: str) -> str:
    prompt = (
        "Summarize the following text into a concise, readable summary. "
        "Keep the key ideas, remove repetition, and format it well for students.\n\n"
        f"Text: {text}"
    )
    return call_gemini(prompt)
