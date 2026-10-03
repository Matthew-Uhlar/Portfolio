import { useEffect, useState } from 'react'
import { api } from '../api'
import { useProject } from '../hooks'
import type { WorkItem, WorkStatus } from '../types'

const columns: { status: WorkStatus; label: string }[] = [
  { status: 'Ready', label: 'Ready' },
  { status: 'InProgress', label: 'In Progress' },
  { status: 'Review', label: 'Review' },
  { status: 'Done', label: 'Done' }
]

export default function Board() {
  const { project } = useProject()
  const [items, setItems] = useState<WorkItem[]>([])

  useEffect(() => {
    if (project) {
      api<WorkItem[]>(`/work-items/project/${project.id}`).then(setItems)
    }
  }, [project])

  async function move(item: WorkItem, status: WorkStatus) {
    const updated = await api<WorkItem>(`/work-items/${item.id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status })
    })
    setItems(current => current.map(existing => existing.id === updated.id ? updated : existing))
  }

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">Current sprint</span>
          <h2>Sprint Board</h2>
          <p>Move work forward as the team makes progress.</p>
        </div>
      </header>

      <section className="board">
        {columns.map(column => (
          <div
            className="board-column"
            key={column.status}
            onDragOver={event => event.preventDefault()}
            onDrop={event => {
              const id = Number(event.dataTransfer.getData('workItemId'))
              const item = items.find(value => value.id === id)
              if (item) move(item, column.status)
            }}
          >
            <div className="column-header">
              <h3>{column.label}</h3>
              <span>{items.filter(item => item.status === column.status).length}</span>
            </div>

            {items.filter(item => item.status === column.status).map(item => (
              <article
                className="work-card"
                draggable
                onDragStart={event => event.dataTransfer.setData('workItemId', item.id.toString())}
                key={item.id}
              >
                <div className="card-topline">
                  <span className={`priority ${item.priority.toLowerCase()}`}>{item.priority}</span>
                  <strong>{item.storyPoints} pts</strong>
                </div>
                <h4>{item.title}</h4>
                <p>{item.description}</p>
                <small>{item.assignee || 'Unassigned'}</small>
              </article>
            ))}
          </div>
        ))}
      </section>
    </>
  )
}
