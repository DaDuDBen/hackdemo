"""State transition rules for Invoice status updates."""
from app.models.enums import InvoiceStatus

ALLOWED_STATUS_TRANSITIONS: dict[InvoiceStatus, set[InvoiceStatus]] = {
    InvoiceStatus.DRAFT: {InvoiceStatus.ACTIVE, InvoiceStatus.CLOSED},
    InvoiceStatus.ACTIVE: {
        InvoiceStatus.PAID,
        InvoiceStatus.DISPUTED,
        InvoiceStatus.ESCALATION_READY,
        InvoiceStatus.CLOSED,
    },
    InvoiceStatus.DISPUTED: {InvoiceStatus.ACTIVE, InvoiceStatus.CLOSED},
    InvoiceStatus.ESCALATION_READY: {InvoiceStatus.ESCALATED, InvoiceStatus.PAID, InvoiceStatus.CLOSED},
    InvoiceStatus.ESCALATED: {InvoiceStatus.PAID, InvoiceStatus.CLOSED},
    InvoiceStatus.PAID: {InvoiceStatus.CLOSED},
    InvoiceStatus.CLOSED: set(),
}


def can_transition(current_status: InvoiceStatus, target_status: InvoiceStatus) -> bool:
    """Return True when state transition is legal based on business state machine."""
    return target_status in ALLOWED_STATUS_TRANSITIONS.get(current_status, set())
