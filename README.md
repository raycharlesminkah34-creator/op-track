# OP-TRACK — Opportunity Tracker

A full-stack application for tracking job, internship, scholarship, and graduate program opportunities.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite |
| Backend | FastAPI |
| Database | SQLite (development) |
| ORM | SQLAlchemy 2.0 |
| Validation | Pydantic v2 |
| Testing | pytest |

## Getting Started

### Backend

```bash
cd backend
.\.venv\Scripts\activate
uvicorn app.main:app --reload
```

- API Base URL: `http://localhost:8000`
- Interactive Swagger Docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### Running Backend Tests

```bash
cd backend
pytest -v
```

### Frontend (when ready)

```bash
cd frontend
npm install
npm run dev
```

- Web UI: `http://localhost:5173`
- API calls proxy automatically to `http://localhost:8000` via Vite dev proxy.
