import json
import os
from urllib import error, request

from dotenv import load_dotenv

load_dotenv()


def _get_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")
    return api_key


def _get_model_names() -> list[str]:
    configured = os.getenv("GEMINI_MODEL", "").strip()
    candidates: list[str] = []

    if configured:
        candidates.append(configured)

    for model_name in [
        "gemini-2.0-flash-lite",
        "gemini-2.0-flash",
        "gemini-2.5-flash",
        "gemini-3.6-flash",
    ]:
        if model_name not in candidates:
            candidates.append(model_name)

    return candidates


def _offline_fallback(prompt: str) -> str:
    """Keep the local learning tools usable when the provider quota is exhausted."""
    content = prompt.split("\n\n", 1)[-1].strip()
    return (
        "## Offline mode\n\n"
        "Google AI is temporarily unavailable because the configured API quota "
        "has been reached. Your request was received successfully:\n\n"
        f"> {content}\n\n"
        "Add a working Gemini API key or wait for the quota to reset to receive "
        "a generated answer."
    )


def call_gemini(prompt: str) -> str:
    api_key = _get_api_key()
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    last_error = None

    for model_name in _get_model_names():
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model_name}:generateContent?key={api_key}"
        )
        req = request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            last_error = RuntimeError(f"Model {model_name} failed: {detail}")
            if exc.code in (404, 429, 503):
                continue
            raise last_error from exc
        except Exception as exc:
            last_error = RuntimeError(f"Gemini API request failed for model {model_name}: {exc}")
            raise last_error from exc

        if "candidates" not in data or not data["candidates"]:
            raise RuntimeError(f"Gemini returned no candidate content for model {model_name}.")

        parts = data["candidates"][0].get("content", {}).get("parts", [])
        text = "".join(part.get("text", "") for part in parts if isinstance(part, dict))

        if not text.strip():
            raise RuntimeError(f"Gemini returned empty content for model {model_name}.")

        return text.strip()

    if os.getenv("GEMINI_OFFLINE_FALLBACK", "true").lower() in {"1", "true", "yes"}:
        return _offline_fallback(prompt)

    raise last_error or RuntimeError("No Gemini model was available to serve this request.")
