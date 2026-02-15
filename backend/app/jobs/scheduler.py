"""Daily cron-style automation for reminders and escalation actions."""
from __future__ import annotations

from datetime import date, datetime, timedelta

from sqlalchemy import and_, select

from app.db.session import SessionLocal
from app.models.enums import InvoiceStatus, ReminderStage
from app.models.invoice import Invoice
from app.models.reminder_log import ReminderLog
from app.services.ai_service import ai_service
from app.services.email_service import send_email
from app.services.legal_templates import render_escalation_template
from app.services.rule_engine import MAX_AUTOMATED_REMINDERS, process_invoice


def _idempotency_key(invoice_id: int, action_type: str, on_date: date) -> str:
    return f"{invoice_id}:{action_type}:{on_date.isoformat()}"


def run_daily_scheduler(today: date | None = None) -> dict[str, int]:
    """Process invoices due for action. Idempotent per invoice/action/day."""
    run_day = today or date.today()
    sent_reminders = 0
    generated_escalations = 0

    db = SessionLocal()
    try:
        invoices = db.scalars(
            select(Invoice).where(
                and_(
                    Invoice.status.in_([InvoiceStatus.ACTIVE, InvoiceStatus.ESCALATION_READY]),
                    Invoice.next_action_date.is_not(None),
                    Invoice.next_action_date <= run_day,
                )
            )
        ).all()

        for invoice in invoices:
            result = process_invoice(invoice, as_of=run_day)

            if invoice.status in {InvoiceStatus.PAID, InvoiceStatus.CLOSED}:
                continue

            if invoice.reminder_count < MAX_AUTOMATED_REMINDERS:
                action_type = "reminder"
                key = _idempotency_key(invoice.id, action_type, run_day)
                exists = db.scalar(select(ReminderLog).where(ReminderLog.idempotency_key == key))
                if exists:
                    continue

                ai_text = ai_service.generate_reminder(invoice, result.stage, result.overdue_days)
                subject = f"Payment Reminder - Invoice {invoice.invoice_number}"
                send_email(invoice.customer_email, subject, ai_text.content)

                db.add(
                    ReminderLog(
                        invoice_id=invoice.id,
                        stage=result.stage,
                        channel="email",
                        recipient=invoice.customer_email,
                        subject=subject,
                        body=ai_text.content,
                        action_type=action_type,
                        idempotency_key=key,
                    )
                )
                invoice.reminder_count += 1
                invoice.last_reminder_at = datetime.utcnow()
                invoice.next_action_date = run_day + timedelta(days=7)
                sent_reminders += 1

            if result.stage == ReminderStage.ESCALATION_READY and invoice.escalation_consent:
                action_type = "escalation"
                key = _idempotency_key(invoice.id, action_type, run_day)
                exists = db.scalar(select(ReminderLog).where(ReminderLog.idempotency_key == key))
                if exists:
                    continue

                draft = render_escalation_template(invoice, result.interest_amount, today_iso=run_day.isoformat())
                polished = ai_service.generate_legal_draft(invoice, result.interest_amount, draft)

                db.add(
                    ReminderLog(
                        invoice_id=invoice.id,
                        stage=result.stage,
                        channel="system",
                        recipient=invoice.customer_email,
                        subject=f"Escalation Draft - Invoice {invoice.invoice_number}",
                        body=polished.content,
                        action_type=action_type,
                        idempotency_key=key,
                    )
                )
                invoice.status = InvoiceStatus.ESCALATED
                invoice.next_action_date = None
                generated_escalations += 1

        db.commit()
    finally:
        db.close()

    return {"reminders_sent": sent_reminders, "escalations_generated": generated_escalations}
