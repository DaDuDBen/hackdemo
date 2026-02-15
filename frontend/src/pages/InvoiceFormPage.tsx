import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createInvoice } from '../api/invoices'

export default function InvoiceFormPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    invoice_number: '',
    customer_name: '',
    customer_email: '',
    issue_date: '',
    due_date: '',
    amount_due: 0,
    currency: 'INR',
    escalation_consent: false,
  })

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    await createInvoice(form)
    navigate('/')
  }

  return (
    <form onSubmit={submit}>
      <h2>Create Invoice</h2>
      <input placeholder="Invoice #" onChange={(e) => setForm({ ...form, invoice_number: e.target.value })} required />
      <input placeholder="Customer" onChange={(e) => setForm({ ...form, customer_name: e.target.value })} required />
      <input placeholder="Email" type="email" onChange={(e) => setForm({ ...form, customer_email: e.target.value })} required />
      <label>Issue date <input type="date" onChange={(e) => setForm({ ...form, issue_date: e.target.value })} required /></label>
      <label>Due date <input type="date" onChange={(e) => setForm({ ...form, due_date: e.target.value })} required /></label>
      <label>Amount <input type="number" step="0.01" onChange={(e) => setForm({ ...form, amount_due: Number(e.target.value) })} required /></label>
      <label>
        <input type="checkbox" onChange={(e) => setForm({ ...form, escalation_consent: e.target.checked })} /> Escalation consent
      </label>
      <button type="submit">Create</button>
    </form>
  )
}
