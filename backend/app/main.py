"""FastAPI entrypoint for the Invoice Escalation System."""
from fastapi import FastAPI

from app.api import invoices_router, system_router
from app.core.config import settings
from app.db import init_db

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


app.include_router(invoices_router)
app.include_router(system_router)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
