# AI-Powered Automated Invoice Escalation System (MSMEs)

Complete local implementation scaffold (backend + frontend + scheduler + AI wrapper + escalation draft flow).

## What is implemented

- ✅ Stage 1: project structure
- ✅ Stage 2: SQLite models and state transitions
- ✅ Stage 3: deterministic rule engine
- ✅ Stage 4: invoice REST API
- ✅ Stage 5: AI integration layer (LLM-agnostic wrapper)
- ✅ Stage 6: daily automation scheduler with idempotency
- ✅ Stage 7: SMTP email sending module
- ✅ Stage 8: React frontend pages (form/list/detail/timeline)
- ✅ Stage 9: legal escalation template + AI polish hook
- ✅ Stage 10: demo scripts for seed + 50-day escalation simulation

## Project structure

```text
backend/app/
├── api/
│   ├── invoices.py
│   └── system.py
├── core/
│   └── config.py
├── db/
│   ├── base.py
│   ├── init_db.py
│   └── session.py
├── jobs/
│   └── scheduler.py
├── models/
│   ├── enums.py
│   ├── invoice.py
│   ├── reminder_log.py
│   └── state_machine.py
├── schemas/
│   └── invoice.py
├── services/
│   ├── ai_service.py
│   ├── email_service.py
│   ├── legal_templates.py
│   └── rule_engine.py
└── main.py

frontend/src/
├── api/
├── components/
├── pages/
├── types/
├── App.tsx
└── main.tsx

scripts/
├── run_scheduler.py
└── seed_demo.py
```

## Run backend (you need to do this locally)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend docs: `http://localhost:8000/docs`

## Run frontend (you need to do this locally)

```bash
cd frontend
npm install
npm run dev
```

Frontend app: `http://localhost:5173`

## API endpoints

- `POST /invoices`
- `GET /invoices`
- `GET /invoices/{id}`
- `POST /invoices/{id}/mark-paid`
- `GET /invoices/{id}/timeline`
- `POST /system/run-daily-job` (manual scheduler trigger)

## Rule definitions

- `0–7 days overdue` → Gentle
- `8–30 days overdue` → Firm
- `31–45 days overdue` → Pre-Escalation
- `>45 days overdue` → Escalation Ready

Interest is deterministic (simple prorated) and **not AI-controlled**.

## AI guardrails

AI is used only for:
- reminder text generation
- legal draft polishing

AI is not used for:
- stage determination
- interest calculation
- escalation eligibility

## Demo flow (you need to do this locally)

### 1) Seed DB with a 50-day overdue invoice

```bash
PYTHONPATH=backend python scripts/seed_demo.py
```

### 2) Trigger daily scheduler

```bash
PYTHONPATH=backend python scripts/run_scheduler.py
```

Or via API:

```bash
curl -X POST http://localhost:8000/system/run-daily-job
```

### 3) Inspect timeline and escalation status

```bash
curl http://localhost:8000/invoices
curl http://localhost:8000/invoices/1
curl http://localhost:8000/invoices/1/timeline
```

## Notes on environment

If SMTP/AI credentials are missing, fill `.env` before expecting real email/provider behavior.
This repo is designed for local execution first; production hardening (auth, retries, monitoring, migrations) can be layered next.
