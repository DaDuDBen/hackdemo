"""LLM-agnostic AI wrapper for reminder and legal draft text generation.

Guardrail: AI only generates/polishes text. It never decides business logic.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from string import Template

import httpx

from app.core.config import settings
from app.models.enums import ReminderStage
from app.models.invoice import Invoice


@dataclass
class AITextResult:
    content: str
    provider: str
    model: str


REMINDER_PROMPT = Template(
    """
You are a professional accounts receivable assistant.
Write a concise payment reminder email.

Constraints:
- Keep it under 180 words.
- Professional, non-threatening tone.
- Mention invoice number, amount, due date, overdue days, and stage.
- Ask for confirmation of payment date.

Invoice:
- Number: $invoice_number
- Customer: $customer_name
- Amount: $amount_due $currency
- Due date: $due_date
- Overdue days: $overdue_days
- Stage: $stage

Return plain text only.
""".strip()
)

LEGAL_DRAFT_POLISH_PROMPT = Template(
    """
Polish the following legal notice draft for clarity and formality without changing facts or numbers.
Keep placeholders intact if present.

Invoice details:
- Invoice Number: $invoice_number
- Customer: $customer_name
- Principal: $amount_due $currency
- Interest: $interest_amount $currency

Draft:
$draft

Return plain text only.
""".strip()
)


class AIService:
    """Provider wrapper with safe fallback when AI APIs are unavailable."""

    def __init__(self) -> None:
        self.provider = settings.ai_provider
        self.model = settings.ai_model
        self.base_url = settings.ai_base_url
        self.api_key = settings.ai_api_key

    def _call_provider(self, prompt: str) -> str:
        """Best-effort provider call; falls back to deterministic output on failure."""
        if not self.api_key:
            return "[AI disabled] " + prompt.splitlines()[-1]

        try:
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a careful business writing assistant."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
            }
            # OpenAI-compatible chat completions endpoint.
            with httpx.Client(timeout=20.0) as client:
                response = client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
        except Exception:
            return "[AI fallback] Generated message unavailable from provider; please review manually."

    def generate_reminder(self, invoice: Invoice, stage: ReminderStage, overdue_days: int) -> AITextResult:
        """Generate reminder text. Business stage is an input, never AI-computed."""
        prompt = REMINDER_PROMPT.substitute(
            invoice_number=invoice.invoice_number,
            customer_name=invoice.customer_name,
            amount_due=str(invoice.amount_due),
            currency=invoice.currency,
            due_date=invoice.due_date.isoformat(),
            overdue_days=overdue_days,
            stage=stage.value,
        )
        content = self._call_provider(prompt)
        return AITextResult(content=content, provider=self.provider, model=self.model)

    def generate_legal_draft(self, invoice: Invoice, interest: Decimal, draft_template: str) -> AITextResult:
        """Polish legal draft text without changing principal facts."""
        prompt = LEGAL_DRAFT_POLISH_PROMPT.substitute(
            invoice_number=invoice.invoice_number,
            customer_name=invoice.customer_name,
            amount_due=str(invoice.amount_due),
            currency=invoice.currency,
            interest_amount=str(interest),
            draft=draft_template,
        )
        content = self._call_provider(prompt)
        return AITextResult(content=content, provider=self.provider, model=self.model)


ai_service = AIService()
