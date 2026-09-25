# EduGenie AI

**Study smarter with AI.**

EduGenie AI is a FastAPI web application that gives students one place to ask questions, understand concepts, generate quizzes, summarize notes, and create personalized learning paths using Google Gemini.

## Features

- Question and answer assistant
- Student-friendly concept explanations
- Automatic quiz generation
- Notes summarization
- Learning recommendations
- Input validation and service-error handling
- Offline fallback when Gemini quota is unavailable
- Responsive browser interface

## Technology

- Python
- FastAPI and Uvicorn
- Jinja2 templates
- HTML, CSS, and JavaScript
- Google Gemini API

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:GEMINI_API_KEY = "your-api-key"
python main.py
```

Open http://127.0.0.1:8002/ in a browser. Set the `PORT` environment variable to use another port.

## API Routes

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/` | Web interface |
| `GET` | `/health` | Health check |
| `POST` | `/qa` | Answer a question |
| `POST` | `/explain` | Explain a concept |
| `POST` | `/quiz` | Generate a quiz |
| `POST` | `/summarize` | Summarize text |
| `POST` | `/learn/recommendations` | Create a learning path |

POST requests use this JSON shape:

```json
{"text": "What is photosynthesis?"}
```

## Testing

```powershell
python -m unittest discover -s tests -v
```

## Project Lifecycle Documentation

The complete project record covers:

1. Brainstorming and ideation
2. Requirement analysis
3. Project design
4. Project planning
5. Project development
6. Project testing
7. Project documentation
8. Project demonstration

Read the full record in [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md).

## Security Note

Keep API keys in environment variables or a local `.env` file. Never commit real keys to the repository.
