"""Invoice ORM model."""
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Enum, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import InvoiceStatus, ReminderStage


class Invoice(Base):
    """Stores invoice financial data and collection workflow state."""

    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    invoice_number: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)

    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_email: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_phone: Mapped[str | None] = mapped_column(String(32), nullable=True)

    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    amount_due: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), default="INR", nullable=False)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[InvoiceStatus] = mapped_column(
        Enum(InvoiceStatus),
        default=InvoiceStatus.ACTIVE,
        nullable=False,
        index=True,
    )
    current_stage: Mapped[ReminderStage] = mapped_column(
        Enum(ReminderStage),
        default=ReminderStage.GENTLE,
        nullable=False,
    )

    reminder_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_reminder_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    next_action_date: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)

    escalation_consent: Mapped[bool] = mapped_column(default=False, nullable=False)
    escalation_generated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    reminder_logs = relationship("ReminderLog", back_populates="invoice", cascade="all, delete-orphan")
