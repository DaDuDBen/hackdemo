import type { TimelineItem } from '../types/invoice'

export default function Timeline({ items }: { items: TimelineItem[] }) {
  if (!items.length) return <p>No reminders/escalation events yet.</p>
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>
          <strong>{item.sent_at}</strong> [{item.action_type}] {item.subject}
        </li>
      ))}
    </ul>
  )
}
