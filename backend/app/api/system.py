"""System endpoints for scheduler triggering and diagnostics."""
from fastapi import APIRouter

from app.jobs.scheduler import run_daily_scheduler

router = APIRouter(prefix="/system", tags=["system"])


@router.post("/run-daily-job")
def run_daily_job() -> dict[str, int]:
    """Manually trigger daily automation job for local testing."""
    return run_daily_scheduler()
