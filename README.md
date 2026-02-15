# AI-Powered Automated Invoice Escalation System (MSMEs)

This repository is being built in staged increments. Stage 1 provides a production-style project scaffold with FastAPI backend and React frontend foundations.

## Stage 1 Deliverables

- Modular folder structure for backend, frontend, scripts, and docs.
- Python dependencies and frontend package manifest.
- Environment variable template for app, DB, scheduler, SMTP, and AI provider configs.
- Minimal FastAPI app with health endpoint.
- Local setup instructions.

## Repository structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── jobs/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   ├── tests/
│   └── README.md
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── types/
│   │   └── utils/
│   ├── package.json
│   └── README.md
├── scripts/
├── docs/
├── .env.example
├── requirements.txt
└── README.md
```

## Backend setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

## Stage-by-stage implementation

- Stage 1: Project structure ✅
- Stage 2+: Database, rule engine, APIs, AI layer, automation, email, UI, escalation template, demo flow (in upcoming commits/stages).
