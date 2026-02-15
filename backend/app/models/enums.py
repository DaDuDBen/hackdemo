"""Domain enums for invoice workflow stages and statuses."""
from enum import StrEnum


class InvoiceStatus(StrEnum):
    """Lifecycle states for an invoice."""

    DRAFT = "draft"
    ACTIVE = "active"
    PAID = "paid"
    DISPUTED = "disputed"
    ESCALATION_READY = "escalation_ready"
    ESCALATED = "escalated"
    CLOSED = "closed"


class ReminderStage(StrEnum):
    """Rule engine output stages based on overdue days."""

    GENTLE = "gentle"
    FIRM = "firm"
    PRE_ESCALATION = "pre_escalation"
    ESCALATION_READY = "escalation_ready"
