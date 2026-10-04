import { label, type TicketPriority, type TicketStatus } from '../types'

export function StatusBadge({ status }: { status: TicketStatus }) {
  return <span className={`badge status-${status.toLowerCase()}`}>{label(status)}</span>
}

export function PriorityBadge({ priority }: { priority: TicketPriority }) {
  return <span className={`badge priority-${priority.toLowerCase()}`}>{label(priority)}</span>
}

export function formatDate(value: string | null) {
  return value
    ? new Date(value).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' })
    : ''
}
