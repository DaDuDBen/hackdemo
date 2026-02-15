"""Seed demo invoices including a 50-day overdue case."""
from datetime import date, timedelta
from decimal import Decimal

from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models.invoice import Invoice


def seed() -> None:
    init_db()
    db = SessionLocal()
    try:
        demo = [
            Invoice(
                invoice_number="INV-1001",
                customer_name="Acme Retail",
                customer_email="finance@acme.test",
                issue_date=date.today() - timedelta(days=60),
                due_date=date.today() - timedelta(days=50),
                amount_due=Decimal("12000.00"),
                currency="INR",
                escalation_consent=True,
                next_action_date=date.today(),
            ),
            Invoice(
                invoice_number="INV-1002",
                customer_name="Beta Traders",
                customer_email="accounts@beta.test",
                issue_date=date.today() - timedelta(days=20),
                due_date=date.today() - timedelta(days=5),
                amount_due=Decimal("5500.00"),
                currency="INR",
                escalation_consent=False,
                next_action_date=date.today(),
            ),
        ]
        for row in demo:
            exists = db.query(Invoice).filter(Invoice.invoice_number == row.invoice_number).first()
            if not exists:
                db.add(row)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Demo invoices seeded.")
