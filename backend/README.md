# Backend (FastAPI)

## Modules

- `services/rule_engine.py` - deterministic business logic
- `services/ai_service.py` - LLM-agnostic text generation wrapper
- `services/email_service.py` - SMTP sender
- `services/legal_templates.py` - legal notice template renderer
- `jobs/scheduler.py` - daily reminder/escalation automation

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
cp ../.env.example ../.env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Manual test

```bash
PYTHONPATH=.. python ../scripts/seed_demo.py
curl -X POST http://localhost:8000/system/run-daily-job
curl http://localhost:8000/invoices
```
