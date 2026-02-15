"""Manual scheduler runner for local cron/testing."""
from app.jobs.scheduler import run_daily_scheduler

if __name__ == "__main__":
    print(run_daily_scheduler())
