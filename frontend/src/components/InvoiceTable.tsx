import { Link } from 'react-router-dom'
import type { InvoiceListItem } from '../types/invoice'

export default function InvoiceTable({ rows }: { rows: InvoiceListItem[] }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Invoice</th>
          <th>Customer</th>
          <th>Amount</th>
          <th>Overdue</th>
          <th>Stage</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((r) => (
          <tr key={r.id}>
            <td>
              <Link to={`/invoices/${r.id}`}>{r.invoice_number}</Link>
            </td>
            <td>{r.customer_name}</td>
            <td>{r.amount_due} {r.currency}</td>
            <td>{r.overdue_days}d</td>
            <td>{r.current_stage}</td>
            <td>
              {r.status}
              {r.current_stage === 'escalation_ready' && <span className="badge">Escalation Ready</span>}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
