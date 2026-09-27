# PocketSmart AI

PocketSmart AI is a FastAPI + Jinja2 GenAI application based on the supplied project documentation. It provides:

- Home Interior Budget Planner
- Party Budget Planner
- Jewelry Budget Planner with optional outfit-image input
- User registration/login/logout
- JWT authentication
- SQLite recommendation history
- Gemini multimodal integration
- Deterministic mock-AI fallback for local testing
- Responsive HTML/CSS/JavaScript UI
- Health endpoint and automated tests

## Architecture

Browser → FastAPI routes → services → Gemini / mock recommender → SQLite history → Jinja2 frontend.

The application uses FastAPI consistently because the documentation's later milestones specify FastAPI, even though early pages also mention Flask.

## Important model note

The original document specifies Gemini 1.5 Flash Pro. The current Gemini API model lifecycle has moved beyond that model, so the code uses a configurable `GEMINI_MODEL`, defaulting to `gemini-3.8-flash`. Change it in `.env` if your account exposes a different supported model.

## Windows + VS Code setup

1. Install Python 3.11+.
2. Extract this folder and open it in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment:

   `python -m venv .venv`

5. Activate it:

   PowerShell:
   `.venv\\Scripts\\Activate.ps1`

   CMD:
   `.venv\\Scripts\\activate`

6. Install packages:

   `pip install -r requirements.txt`

7. Create `.env` from `.env.example`.
8. For a no-key local test, keep:

   `USE_MOCK_AI=true`

9. Start:

   `python -m app.main`

10. Open:

   http://127.0.0.1:8000

11. API docs:

   http://127.0.0.1:8000/docs

## Enable real Gemini

Put your API key in `.env`:

`GEMINI_API_KEY=your_key_here`

Then set:

`USE_MOCK_AI=false`

The jewelry endpoint sends the uploaded image as multimodal input. Never expose the API key in frontend JavaScript.

## Test

With the virtual environment active:

`pytest -q`

Manual smoke test:

1. Register.
2. Login.
3. Open Home / Party / Jewelry.
4. Submit a budget.
5. Confirm recommendations appear.
6. Open History.
7. For Jewelry, optionally upload an image.
8. Check `/api/health`.

## API endpoints

- `POST /api/register`
- `POST /api/login`
- `POST /api/logout`
- `GET /api/session-info`
- `GET /api/session-data`
- `POST /api/generate-home`
- `POST /api/generate-party`
- `POST /api/generate-jewelry`
- `GET /api/recommendations-details`
- `GET /api/history`
- `GET /api/health`

## Platform links

The application deliberately uses search links rather than scraping or claiming live inventory. This keeps the base project reliable without requiring private partner APIs. Replace `app/services/catalog.py` with official affiliate/product APIs if you later obtain authorized credentials.

## Production hardening

Before deployment, change `SECRET_KEY`, use PostgreSQL, configure HTTPS, restrict CORS to the deployed domain, add rate limiting, add CSRF protection if using cookie-only browser authentication, and move secrets to a managed secret store.
