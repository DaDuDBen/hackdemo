"""Pydantic schemas for invoice and reminder timeline records."""
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field

from app.models.enums import InvoiceStatus, ReminderStage


class InvoiceBase(BaseModel):
    invoice_number: str = Field(min_length=1, max_length=64)
    customer_name: str = Field(min_length=1, max_length=255)
    customer_email: EmailStr
    customer_phone: str | None = None
    issue_date: date
    due_date: date
    amount_due: Decimal = Field(gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=8)
    notes: str | None = None


class InvoiceCreate(InvoiceBase):
    escalation_consent: bool = False


class InvoiceRead(InvoiceBase):
    id: int
    status: InvoiceStatus
    current_stage: ReminderStage
    reminder_count: int
    next_action_date: date | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReminderLogRead(BaseModel):
    id: int
    invoice_id: int
    stage: ReminderStage
    channel: str
    recipient: str
    subject: str
    body: str
    action_type: str
    sent_at: datetime

    class Config:
        from_attributes = True
