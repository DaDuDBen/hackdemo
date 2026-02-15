"""Escalation legal notice templates and rendering helpers."""
from __future__ import annotations

from decimal import Decimal
from string import Template

from app.models.invoice import Invoice

ESCALATION_TEMPLATE = Template(
    """
Subject: Final Demand Notice - Invoice $invoice_number

Date: $today

To,
$customer_name

This is a formal notice regarding Invoice $invoice_number, issued on $issue_date and due on $due_date.

Principal Amount Due: $amount_due $currency
Accrued Interest: $interest $currency
Total Outstanding: $total $currency

Despite multiple reminders, payment remains pending. You are requested to clear the outstanding balance within 7 calendar days from receipt of this notice.

If payment is not received within this period, we may initiate legal recovery proceedings as permitted by applicable law, subject to prior approvals.

Please treat this as urgent and confirm payment timeline in writing.

Sincerely,
Accounts Receivable Team
""".strip()
)


def render_escalation_template(invoice: Invoice, interest: Decimal, today_iso: str) -> str:
    """Render a deterministic legal draft prior to optional AI polishing."""
    total = invoice.amount_due + interest
    return ESCALATION_TEMPLATE.substitute(
        invoice_number=invoice.invoice_number,
        today=today_iso,
        customer_name=invoice.customer_name,
        issue_date=invoice.issue_date.isoformat(),
        due_date=invoice.due_date.isoformat(),
        amount_due=str(invoice.amount_due),
        currency=invoice.currency,
        interest=str(interest),
        total=str(total),
    )
