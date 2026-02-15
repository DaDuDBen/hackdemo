export type InvoiceStatus =
  | 'draft'
  | 'active'
  | 'paid'
  | 'disputed'
  | 'escalation_ready'
  | 'escalated'
  | 'closed'

export type ReminderStage = 'gentle' | 'firm' | 'pre_escalation' | 'escalation_ready'

export interface Invoice {
  id: number
  invoice_number: string
  customer_name: string
  customer_email: string
  issue_date: string
  due_date: string
  amount_due: string
  currency: string
  status: InvoiceStatus
  current_stage: ReminderStage
  reminder_count: number
  next_action_date: string | null
  escalation_consent: boolean
  paid_at: string | null
  created_at: string
  updated_at: string
}

export interface InvoiceListItem extends Invoice {
  overdue_days: number
  interest_amount: string
}

export interface InvoiceDetailResponse {
  invoice: Invoice
  overdue_days: number
  interest_amount: string
}

export interface TimelineItem {
  id: number
  stage: ReminderStage
  channel: string
  recipient: string
  subject: string
  body: string
  action_type: string
  sent_at: string
}
