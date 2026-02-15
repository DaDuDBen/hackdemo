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
