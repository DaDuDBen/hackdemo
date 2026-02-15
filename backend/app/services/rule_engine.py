"""Deterministic, rule-based workflow logic for invoice escalation."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from app.models.enums import InvoiceStatus, ReminderStage
from app.models.invoice import Invoice
from app.models.state_machine import can_transition

ANNUAL_INTEREST_RATE = Decimal("0.18")
MAX_AUTOMATED_REMINDERS = 4


@dataclass
class InvoiceProcessingResult:
    """Computed rule outputs for an invoice at a given point in time."""

    overdue_days: int
    stage: ReminderStage
    interest_amount: Decimal


def calculate_days_overdue(due_date: date, as_of: date | None = None) -> int:
    """Return non-negative overdue day count from due date to as_of date."""
    current_day = as_of or date.today()
    delta_days = (current_day - due_date).days
    return max(delta_days, 0)


def determine_stage(overdue_days: int) -> ReminderStage:
    """Map overdue days into collection stage buckets.

    0–7 days      -> gentle
    8–30 days     -> firm
    31–45 days    -> pre_escalation
    >45 days      -> escalation_ready
    """
    if overdue_days <= 7:
        return ReminderStage.GENTLE
    if overdue_days <= 30:
        return ReminderStage.FIRM
    if overdue_days <= 45:
        return ReminderStage.PRE_ESCALATION
    return ReminderStage.ESCALATION_READY


def calculate_interest(amount_due: Decimal, overdue_days: int, annual_rate: Decimal = ANNUAL_INTEREST_RATE) -> Decimal:
    """Simple interest prorated by overdue days.

    Formula: amount * annual_rate * (days / 365)
    """
    if overdue_days <= 0:
        return Decimal("0.00")

    interest = amount_due * annual_rate * (Decimal(overdue_days) / Decimal(365))
    return interest.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def process_invoice(invoice: Invoice, as_of: date | None = None) -> InvoiceProcessingResult:
    """Apply deterministic business logic to invoice fields.

    AI is intentionally not involved in these decisions.
    """
    overdue_days = calculate_days_overdue(invoice.due_date, as_of=as_of)
    stage = determine_stage(overdue_days)
    interest_amount = calculate_interest(invoice.amount_due, overdue_days)

    invoice.current_stage = stage

    if invoice.status not in {InvoiceStatus.PAID, InvoiceStatus.CLOSED}:
        if stage == ReminderStage.ESCALATION_READY and invoice.escalation_consent:
            if can_transition(invoice.status, InvoiceStatus.ESCALATION_READY):
                invoice.status = InvoiceStatus.ESCALATION_READY
        elif invoice.status == InvoiceStatus.DRAFT and can_transition(invoice.status, InvoiceStatus.ACTIVE):
            invoice.status = InvoiceStatus.ACTIVE

    return InvoiceProcessingResult(overdue_days=overdue_days, stage=stage, interest_amount=interest_amount)
