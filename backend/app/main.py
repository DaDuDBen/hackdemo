"""FastAPI entrypoint for the Invoice Escalation System.

Stage 1 intentionally keeps this minimal while we scaffold modules in later stages.
"""
from fastapi import FastAPI

app = FastAPI(title="Invoice Escalation System")


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Simple health endpoint used by local development and smoke checks."""
    return {"status": "ok"}
