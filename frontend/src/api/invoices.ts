import { api } from './client'
import type { InvoiceDetailResponse, InvoiceListItem, TimelineItem } from '../types/invoice'

export interface CreateInvoicePayload {
  invoice_number: string
  customer_name: string
  customer_email: string
  customer_phone?: string
  issue_date: string
  due_date: string
  amount_due: number
  currency: string
  notes?: string
  escalation_consent: boolean
}

export async function fetchInvoices() {
  const { data } = await api.get<InvoiceListItem[]>('/invoices')
  return data
}

export async function createInvoice(payload: CreateInvoicePayload) {
  const { data } = await api.post('/invoices', payload)
  return data
}

export async function fetchInvoice(id: string) {
  const { data } = await api.get<InvoiceDetailResponse>(`/invoices/${id}`)
  return data
}

export async function markInvoicePaid(id: string) {
  const { data } = await api.post(`/invoices/${id}/mark-paid`)
  return data
}

export async function fetchTimeline(id: string) {
  const { data } = await api.get<TimelineItem[]>(`/invoices/${id}/timeline`)
  return data
}
