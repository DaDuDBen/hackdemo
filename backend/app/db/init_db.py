"""Database initialization helper for local/dev runtime."""
from app.db.base import Base
from app.db.session import engine

# Import models so SQLAlchemy metadata is populated before create_all.
from app.models.invoice import Invoice  # noqa: F401
from app.models.reminder_log import ReminderLog  # noqa: F401


def init_db() -> None:
    """Create tables if they do not exist."""
    Base.metadata.create_all(bind=engine)
