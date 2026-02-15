# AI-Powered Automated Invoice Escalation System (MSMEs)

This repository is being built in staged increments.

## Current Progress

- Stage 1: Project structure ✅
- Stage 2: Database + models ✅
- Stage 3: Rule engine ✅
- Stage 4: Backend API ✅

## Stage 3 + 4 Deliverables

- Deterministic rule engine with overdue day, stage, interest, and invoice-processing functions.
- REST API for invoice create/list/detail/mark-paid/timeline.
- JSON response schemas for list/detail/timeline/status update endpoints.

## Repository structure

```text
backend/app/
├── api/
│   └── invoices.py
├── core/
│   └── config.py
├── db/
│   ├── base.py
│   ├── init_db.py
│   └── session.py
├── models/
│   ├── enums.py
│   ├── invoice.py
│   ├── reminder_log.py
│   └── state_machine.py
├── schemas/
│   └── invoice.py
├── services/
│   └── rule_engine.py
└── main.py
```

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
