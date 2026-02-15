# Backend (FastAPI)

This service exposes REST APIs for invoice tracking, reminder automation, and escalation workflows.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
cp ../.env.example ../.env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000/docs for the OpenAPI UI.

## Stage 3 + 4 Highlights

### Rule engine (`app/services/rule_engine.py`)
- `calculate_days_overdue()`
- `determine_stage()`
- `calculate_interest()`
- `process_invoice()`

Stage mapping:
- `0–7` days -> `gentle`
- `8–30` days -> `firm`
- `31–45` days -> `pre_escalation`
- `>45` days -> `escalation_ready`

### API endpoints
- `POST /invoices`
- `GET /invoices`
- `GET /invoices/{id}`
- `POST /invoices/{id}/mark-paid`
- `GET /invoices/{id}/timeline`
