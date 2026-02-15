# AI-Powered Automated Invoice Escalation System (MSMEs)

This repository is being built in staged increments. Stage 1 provided the project scaffold; Stage 2 adds the SQLite data model and state transition foundations.

## Stage 2 Deliverables

- SQLite setup via SQLAlchemy engine/session.
- Invoice and ReminderLog ORM tables.
- Status and stage enums.
- Explicit state transition map.
- DB initialization on FastAPI startup.

## Repository structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── init_db.py
│   │   │   └── session.py
│   │   ├── jobs/
│   │   ├── models/
│   │   │   ├── enums.py
│   │   │   ├── invoice.py
│   │   │   ├── reminder_log.py
│   │   │   └── state_machine.py
│   │   ├── schemas/
│   │   │   └── invoice.py
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   ├── tests/
│   └── README.md
├── frontend/
│   ├── public/
│   ├── src/
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
- Stage 2: Database + models ✅
- Stage 3+: Rule engine, APIs, AI layer, automation, email, UI, escalation template, demo flow.
