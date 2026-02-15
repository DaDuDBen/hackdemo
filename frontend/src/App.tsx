import { Link, Route, Routes } from 'react-router-dom'
import InvoiceFormPage from './pages/InvoiceFormPage'
import InvoiceListPage from './pages/InvoiceListPage'
import InvoiceDetailPage from './pages/InvoiceDetailPage'

export default function App() {
  return (
    <div className="container">
      <h1>Automated Invoice Escalation System</h1>
      <nav>
        <Link to="/">Invoices</Link> | <Link to="/new">New Invoice</Link>
      </nav>
      <Routes>
        <Route path="/" element={<InvoiceListPage />} />
        <Route path="/new" element={<InvoiceFormPage />} />
        <Route path="/invoices/:id" element={<InvoiceDetailPage />} />
      </Routes>
    </div>
  )
}
