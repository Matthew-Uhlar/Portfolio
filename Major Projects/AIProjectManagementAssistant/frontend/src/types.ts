export type Project = {
  id: number
  name: string
  description: string
  goal: string
}

export type Sprint = {
  id: number
  projectId: number
  name: string
  goal: string
  startDate: string
  endDate: string
  isActive: boolean
}

export type WorkStatus = 'Backlog' | 'Ready' | 'InProgress' | 'Review' | 'Done'
export type Priority = 'Low' | 'Medium' | 'High' | 'Critical'

export type WorkItem = {
  id: number
  projectId: number
  sprintId?: number
  title: string
  description: string
  acceptanceCriteria: string
  status: WorkStatus
  priority: Priority
  storyPoints: number
  assignee: string
}

export type DashboardData = {
  totalItems: number
  completedItems: number
  activeItems: number
  backlogPoints: number
  criticalItems: number
  activeSprint?: Sprint
}
