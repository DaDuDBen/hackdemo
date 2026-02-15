import { useEffect, useState } from 'react'
import { fetchInvoices } from '../api/invoices'
import type { InvoiceListItem } from '../types/invoice'
import InvoiceTable from '../components/InvoiceTable'

export default function InvoiceListPage() {
  const [rows, setRows] = useState<InvoiceListItem[]>([])

  useEffect(() => {
    fetchInvoices().then(setRows)
  }, [])

  return (
    <div>
      <h2>Invoice List</h2>
      <InvoiceTable rows={rows} />
    </div>
  )
}
