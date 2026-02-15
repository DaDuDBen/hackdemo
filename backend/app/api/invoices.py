"""Invoice API endpoints for CRUD-like and timeline access."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.enums import InvoiceStatus
from app.models.invoice import Invoice
from app.models.reminder_log import ReminderLog
from app.schemas import (
    InvoiceCreate,
    InvoiceDetailResponse,
    InvoiceListItem,
    InvoiceRead,
    InvoiceTimelineItem,
    MarkPaidResponse,
)
from app.services.rule_engine import process_invoice

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice(payload: InvoiceCreate, db: Session = Depends(get_db)) -> Invoice:
    existing = db.scalar(select(Invoice).where(Invoice.invoice_number == payload.invoice_number))
    if existing:
        raise HTTPException(status_code=409, detail="Invoice number already exists")

    invoice = Invoice(**payload.model_dump())
    result = process_invoice(invoice)
    invoice.next_action_date = invoice.due_date if result.overdue_days == 0 else datetime.utcnow().date()

    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


@router.get("", response_model=list[InvoiceListItem])
def list_invoices(db: Session = Depends(get_db)) -> list[InvoiceListItem]:
    invoices = db.scalars(select(Invoice).order_by(Invoice.created_at.desc())).all()
    response: list[InvoiceListItem] = []

    for invoice in invoices:
        result = process_invoice(invoice)
        response.append(
            InvoiceListItem(
                **InvoiceRead.model_validate(invoice).model_dump(),
                overdue_days=result.overdue_days,
                interest_amount=result.interest_amount,
            )
        )

    db.commit()
    return response


@router.get("/{invoice_id}", response_model=InvoiceDetailResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)) -> InvoiceDetailResponse:
    invoice = db.get(Invoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    result = process_invoice(invoice)
    db.commit()
    db.refresh(invoice)

    return InvoiceDetailResponse(
        invoice=InvoiceRead.model_validate(invoice),
        overdue_days=result.overdue_days,
        interest_amount=result.interest_amount,
    )


@router.post("/{invoice_id}/mark-paid", response_model=MarkPaidResponse)
def mark_invoice_paid(invoice_id: int, db: Session = Depends(get_db)) -> MarkPaidResponse:
    invoice = db.get(Invoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    invoice.status = InvoiceStatus.PAID
    invoice.paid_at = datetime.utcnow()
    invoice.next_action_date = None

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return MarkPaidResponse(id=invoice.id, status=invoice.status, paid_at=invoice.paid_at)


@router.get("/{invoice_id}/timeline", response_model=list[InvoiceTimelineItem])
def get_invoice_timeline(invoice_id: int, db: Session = Depends(get_db)) -> list[InvoiceTimelineItem]:
    invoice = db.get(Invoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    logs = db.scalars(
        select(ReminderLog).where(ReminderLog.invoice_id == invoice_id).order_by(ReminderLog.sent_at.asc())
    ).all()
    return [InvoiceTimelineItem.model_validate(log) for log in logs]
