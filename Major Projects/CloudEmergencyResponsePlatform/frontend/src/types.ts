export type IncidentStatus = 'Reported' | 'Dispatched' | 'OnScene' | 'Contained' | 'Closed'
export type IncidentSeverity = 'Low' | 'Moderate' | 'High' | 'Critical'
export type UnitStatus = 'Available' | 'Assigned' | 'EnRoute' | 'OnScene' | 'Unavailable'

export type IncidentActivity = {
  id: number
  incidentId: number
  message: string
  createdBy: string
  createdAt: string
}

export type ResponseUnit = {
  id: number
  unitName: string
  unitType: string
  radioCode: string
  status: UnitStatus
  currentLocation: string
}

export type IncidentAssignment = {
  id: number
  incidentId: number
  responseUnitId: number
  assignedAt: string
  clearedAt?: string
  responseUnit?: ResponseUnit
}

export type Incident = {
  id: number
  title: string
  description: string
  address: string
  latitude: number
  longitude: number
  status: IncidentStatus
  severity: IncidentSeverity
  reportedAt: string
  closedAt?: string
  assignments: IncidentAssignment[]
  activity: IncidentActivity[]
}

export type DashboardData = {
  activeIncidents: number
  criticalIncidents: number
  availableUnits: number
  assignedUnits: number
  recentlyReported: Incident[]
}
