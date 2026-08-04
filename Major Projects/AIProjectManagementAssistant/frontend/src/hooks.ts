import { useEffect, useState } from 'react'
import { api } from './api'
import type { Project } from './types'

export function useProject() {
  const [project, setProject] = useState<Project | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api<Project[]>('/projects')
      .then(projects => setProject(projects[0] ?? null))
      .finally(() => setLoading(false))
  }, [])

  return { project, loading }
}
