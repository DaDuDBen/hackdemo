import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchInvoice, fetchTimeline, markInvoicePaid } from '../api/invoices'
import type { InvoiceDetailResponse, TimelineItem } from '../types/invoice'
import Timeline from '../components/Timeline'

export default function InvoiceDetailPage() {
  const { id = '' } = useParams()
  const [detail, setDetail] = useState<InvoiceDetailResponse | null>(null)
  const [timeline, setTimeline] = useState<TimelineItem[]>([])

  useEffect(() => {
    fetchInvoice(id).then(setDetail)
    fetchTimeline(id).then(setTimeline)
  }, [id])

  if (!detail) return <p>Loading...</p>

  return (
    <div>
      <h2>Invoice {detail.invoice.invoice_number}</h2>
      <p>Status: {detail.invoice.status}</p>
      <p>Stage: {detail.invoice.current_stage}</p>
      <p>Overdue Days: {detail.overdue_days}</p>
      <p>Interest: {detail.interest_amount} {detail.invoice.currency}</p>
      <button onClick={async () => {
        await markInvoicePaid(id)
        const refreshed = await fetchInvoice(id)
        setDetail(refreshed)
      }}>Mark Paid</button>
      <h3>Timeline</h3>
      <Timeline items={timeline} />
    </div>
  )
}
