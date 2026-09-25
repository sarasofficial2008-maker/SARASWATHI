import os
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description="AI-powered educational learning assistant"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# -----------------------------
# Request Model
# -----------------------------

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


# -----------------------------
# Home Page
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {}
    )


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "EduGenie"
    }


# -----------------------------
# Question Answering
# -----------------------------

@app.post("/qa")
async def qa(payload: TextRequest):

    try:

        result = answer_question(
            payload.text
        )

        return {
            "result": result
        }

    except Exception as exc:
        message = str(exc)
        if "quota" in message.lower() or "unavailable" in message.lower() or "429" in message or "503" in message:
            raise HTTPException(
                status_code=503,
                detail="The AI service is temporarily unavailable or quota-limited. Please try again in a moment."
            ) from exc

        raise HTTPException(
            status_code=500,
            detail=message
        ) from exc


# -----------------------------
# Explain Concept
# -----------------------------

@app.post("/explain")
async def explain(payload: TextRequest):

    try:

        result = explain_concept(
            payload.text
        )

        return {
            "result": result
        }

    except Exception as exc:
        message = str(exc)
        if "quota" in message.lower() or "unavailable" in message.lower() or "429" in message or "503" in message:
            raise HTTPException(
                status_code=503,
                detail="The AI service is temporarily unavailable or quota-limited. Please try again in a moment."
            ) from exc

        raise HTTPException(
            status_code=500,
            detail=message
        ) from exc


# -----------------------------
# Generate Quiz
# -----------------------------

@app.post("/quiz")
async def quiz(payload: TextRequest):

    try:

        result = generate_quiz(
            payload.text
        )

        return JSONResponse(
            content={
                "result": result
            }
        )

    except Exception as exc:
        message = str(exc)
        if "quota" in message.lower() or "unavailable" in message.lower() or "429" in message or "503" in message:
            raise HTTPException(
                status_code=503,
                detail="The AI service is temporarily unavailable or quota-limited. Please try again in a moment."
            ) from exc

        raise HTTPException(
            status_code=500,
            detail=message
        ) from exc


# -----------------------------
# Summarize
# -----------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):

    try:

        result = summarize_text(
            payload.text
        )

        return {
            "result": result
        }

    except Exception as exc:
        message = str(exc)
        if "quota" in message.lower() or "unavailable" in message.lower() or "429" in message or "503" in message:
            raise HTTPException(
                status_code=503,
                detail="The AI service is temporarily unavailable or quota-limited. Please try again in a moment."
            ) from exc

        raise HTTPException(
            status_code=500,
            detail=message
        ) from exc


# -----------------------------
# Learning Recommendations
# -----------------------------

@app.post("/learn/recommendations")
async def recommendations(payload: TextRequest):

    try:

        result = get_learning_recommendations(
            payload.text
        )

        return {
            "result": result
        }

    except Exception as exc:
        message = str(exc)
        if "quota" in message.lower() or "unavailable" in message.lower() or "429" in message or "503" in message:
            raise HTTPException(
                status_code=503,
                detail="The AI service is temporarily unavailable or quota-limited. Please try again in a moment."
            ) from exc

        raise HTTPException(
            status_code=500,
            detail=message
        ) from exc


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8002"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)