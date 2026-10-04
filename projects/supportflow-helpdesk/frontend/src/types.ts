export type Role = 'EMPLOYEE' | 'TECHNICIAN' | 'ADMIN'
export type TicketStatus = 'OPEN' | 'ASSIGNED' | 'IN_PROGRESS' | 'WAITING_ON_USER' | 'RESOLVED' | 'CLOSED'
export type TicketPriority = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'

export const statuses: TicketStatus[] = ['OPEN', 'ASSIGNED', 'IN_PROGRESS', 'WAITING_ON_USER', 'RESOLVED', 'CLOSED']
export const priorities: TicketPriority[] = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']

export type Person = {
  id: number
  name: string
  email: string
  role: Role
}

export type Comment = {
  id: number
  author: Person
  message: string
  internal: boolean
  createdAt: string
}

export type HistoryEntry = {
  id: number
  changedBy: Person
  changeDescription: string
  createdAt: string
}

export type Ticket = {
  id: number
  title: string
  description: string
  priority: TicketPriority
  status: TicketStatus
  createdBy: Person
  assignedTo: Person | null
  createdAt: string
  updatedAt: string
  resolvedAt: string | null
  comments: Comment[]
  history: HistoryEntry[]
}

export type Dashboard = {
  totalTickets: number
  openTickets: number
  criticalTickets: number
  resolvedTickets: number
}

export type AssignableUser = { id: number; name: string; role: Role }

export type Session = { token: string; name: string; role: Role }

export function label(value: string) {
  return value.charAt(0) + value.slice(1).toLowerCase().replace(/_/g, ' ')
}
