"""ReminderLog ORM model for action timeline and auditability."""
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ReminderStage


class ReminderLog(Base):
    """Captures each reminder/escalation action performed by the system."""

    __tablename__ = "reminder_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id", ondelete="CASCADE"), index=True)

    stage: Mapped[ReminderStage] = mapped_column(Enum(ReminderStage), nullable=False)
    channel: Mapped[str] = mapped_column(String(32), default="email", nullable=False)
    recipient: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    action_type: Mapped[str] = mapped_column(String(32), default="reminder", nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)

    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    invoice = relationship("Invoice", back_populates="reminder_logs")
