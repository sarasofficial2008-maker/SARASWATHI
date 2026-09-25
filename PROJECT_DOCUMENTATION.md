# EduGenie AI Project Documentation

EduGenie AI is a web-based learning assistant that helps students ask questions, understand concepts, generate quizzes, summarize notes, and create learning paths. The application uses a FastAPI backend, a browser-based frontend, and the Google Gemini API.

## 1. Brainstorming and Ideation Phase

### Problem

Students often need several separate tools to study: a question-answering tool, a concept explainer, a summarizer, a quiz generator, and a study planner. Switching between tools makes learning slower and less consistent.

### Proposed idea

Create one simple learning workspace where a student enters a topic or notes and selects the type of help required.

### Main ideas considered

- Question and answer assistant
- Student-friendly concept explanations
- Automatic quiz generation
- Notes summarization
- Personalized learning recommendations
- A lightweight interface that works on desktop and mobile

### Selected idea

EduGenie combines all five learning tools behind one interface. The design keeps the student workflow short: choose a tool, enter content, generate a result, and review the response.

## 2. Requirement Analysis Phase

### Functional requirements

1. The system must display a home page with the available learning tools.
2. The user must be able to enter a question, topic, or notes.
3. The system must support question answering through `/qa`.
4. The system must support concept explanations through `/explain`.
5. The system must generate quizzes through `/quiz`.
6. The system must summarize text through `/summarize`.
7. The system must generate learning recommendations through `/learn/recommendations`.
8. The system must validate empty and excessively long input.
9. The system must report AI service failures without crashing the web server.
10. The system must provide a health check through `/health`.

### Non-functional requirements

- The interface should be simple enough for a student to use without training.
- API responses should be returned as JSON.
- The API key must be loaded from environment configuration, not hard-coded.
- The application should run locally with one command.
- The application should remain usable with an offline fallback when Gemini quota is unavailable.
- User input should be escaped before being inserted into the result page.

### Scope

The current version is a single-user learning assistant. Authentication, persistent user accounts, saved study history, and database storage are outside the current scope.

## 3. Project Design Phase

### Architecture

```text
Browser UI
    |
    | JSON POST request
    v
FastAPI application (main.py)
    |
    +-- qna.py
    +-- explanation_module.py
    +-- quiz_module.py
    +-- summary_module.py
    +-- learning_path.py
            |
            v
      gemini_client.py
            |
            v
      Google Gemini API
```

### Components

- `templates/index.html`: page structure and learning-tool controls.
- `static/css/style.css`: responsive visual styling.
- `static/js/app.js`: input validation, API calls, error display, and response formatting.
- `main.py`: FastAPI application, routes, validation, static files, and templates.
- Feature modules: small prompt-building functions for each learning task.
- `gemini_client.py`: API-key loading, model fallback, Gemini requests, and offline fallback.

### Data flow

1. The user selects a learning tool and enters text.
2. The browser sends `{ "text": "..." }` to the matching API route.
3. FastAPI validates the request using `TextRequest`.
4. The feature module builds a task-specific prompt.
5. `gemini_client.py` calls an available Gemini model.
6. The API returns `{ "result": "..." }`.
7. The browser formats the result and displays it.

## 4. Project Planning Phase

### Work plan

| Work item | Result | Status |
| --- | --- | --- |
| Define the learning-assistant problem | Product concept and scope | Complete |
| Design the API and feature modules | FastAPI routes and Python modules | Complete |
| Build the browser interface | HTML, CSS, and JavaScript UI | Complete |
| Connect Gemini | Configurable API client and model fallback | Complete |
| Add local fallback behavior | Usable response when quota is exhausted | Complete |
| Add automated tests | Import and smoke coverage | In progress |
| Prepare user documentation | Setup and eight-phase record | Complete |
| Record demonstration | Browser walkthrough or project video | To do |

### Suggested milestones

1. **Milestone 1:** Confirm the idea, users, requirements, and screen flow.
2. **Milestone 2:** Implement the FastAPI routes and feature modules.
3. **Milestone 3:** Implement and style the frontend.
4. **Milestone 4:** Connect Gemini and add error handling.
5. **Milestone 5:** Test every route and prepare the demonstration.

## 5. Project Development Phase

### Implemented features

- FastAPI web server with an HTML home page.
- Five learning modes in one interface.
- Pydantic validation for text input from 1 to 20,000 characters.
- Gemini model selection with configurable `GEMINI_MODEL`.
- API-key configuration through `GEMINI_API_KEY`.
- Offline fallback controlled by `GEMINI_OFFLINE_FALLBACK`.
- Friendly handling for quota and temporary service failures.
- Escaped browser output to reduce HTML injection risk.
- Health endpoint for checking server availability.

### Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:GEMINI_API_KEY = "your-api-key"
python main.py
```

Open `http://127.0.0.1:8002/` in a browser. The default port can be changed with the `PORT` environment variable.

## 6. Project Testing Phase

### Current verification

Run the smoke test suite with:

```powershell
python -m unittest discover -s tests -v
```

The existing test verifies that the application and all feature modules import successfully.

### Manual acceptance checklist

- [ ] `GET /` displays the EduGenie interface.
- [ ] `GET /health` returns status `ok`.
- [ ] Each selector option sends its request to the correct route.
- [ ] Empty input shows a validation message without making a request.
- [ ] Valid input displays a generated result.
- [ ] Missing or exhausted Gemini access produces a readable error or offline response.
- [ ] Input longer than 20,000 characters is rejected by the API.
- [ ] The interface remains usable on a narrow mobile viewport.

### Recommended next tests

- Add FastAPI `TestClient` tests for all six API routes.
- Mock `call_gemini` so tests do not depend on network access or API quota.
- Add tests for invalid, empty, and maximum-length payloads.
- Add a browser test for selecting a tool, submitting text, and rendering output.

## 7. Project Documentation Phase

The project documentation should contain:

- Product purpose and target users.
- Functional and non-functional requirements.
- Architecture and data flow.
- Installation and configuration instructions.
- API route descriptions.
- Testing instructions and known limitations.
- Demonstration steps.

This file provides the lifecycle record. The GitHub repository should also include it alongside a concise `README.md`, the source code, tests, and a sanitized example environment file such as `.env.example`. Real API keys must never be committed.

## 8. Project Demonstration Phase

### Demonstration script

1. Start the application with `python main.py`.
2. Open `http://127.0.0.1:8002/`.
3. Enter a question such as `What is photosynthesis?` and select **Question & Answer**.
4. Show the generated response in the Output section.
5. Select **Explain Concept** and submit a short topic.
6. Select **Generate Quiz** and show the structured quiz response.
7. Select **Summarize Text** and paste a short paragraph.
8. Select **Learning Recommendations** and show the study path.
9. Open `/health` to demonstrate server health.
10. Briefly show the tests running successfully.

### Demonstration outcome

The demonstration should prove that EduGenie provides one working interface for multiple AI-assisted study tasks, validates input, handles service limitations, and can be started locally from documented instructions.

## Current Limitations and Future Enhancements

- Responses are not persisted between sessions.
- There is no login or student profile system.
- Quiz answers are generated as text rather than interactive controls.
- The current automated test suite is intentionally small.
- Future versions could add saved history, interactive quizzes, progress tracking, teacher dashboards, and more robust response schemas.