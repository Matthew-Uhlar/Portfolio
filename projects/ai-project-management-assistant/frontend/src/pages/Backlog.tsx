import { FormEvent, useEffect, useState } from 'react'
import { api } from '../api'
import { useProject } from '../hooks'
import type { Priority, WorkItem } from '../types'

export default function Backlog() {
  const { project } = useProject()
  const [items, setItems] = useState<WorkItem[]>([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [priority, setPriority] = useState<Priority>('Medium')
  const [points, setPoints] = useState(3)

  function load() {
    if (project) api<WorkItem[]>(`/work-items/project/${project.id}`).then(setItems)
  }

  useEffect(load, [project])

  async function addItem(event: FormEvent) {
    event.preventDefault()
    if (!project) return

    await api<WorkItem>('/work-items', {
      method: 'POST',
      body: JSON.stringify({
        projectId: project.id,
        sprintId: null,
        title,
        description,
        acceptanceCriteria: '',
        status: 'Backlog',
        priority,
        storyPoints: points,
        assignee: ''
      })
    })

    setTitle('')
    setDescription('')
    load()
  }

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">Future work</span>
          <h2>Backlog</h2>
          <p>Keep upcoming work clear enough that the team can actually plan it.</p>
        </div>
      </header>

      <section className="backlog-layout">
        <form className="panel form-stack" onSubmit={addItem}>
          <h3>Add a work item</h3>
          <label>
            Title
            <input value={title} onChange={event => setTitle(event.target.value)} required />
          </label>
          <label>
            Description
            <textarea value={description} onChange={event => setDescription(event.target.value)} rows={4} required />
          </label>
          <div className="form-row">
            <label>
              Priority
              <select value={priority} onChange={event => setPriority(event.target.value as Priority)}>
                <option>Low</option>
                <option>Medium</option>
                <option>High</option>
                <option>Critical</option>
              </select>
            </label>
            <label>
              Points
              <select value={points} onChange={event => setPoints(Number(event.target.value))}>
                {[1, 2, 3, 5, 8, 13].map(value => <option key={value}>{value}</option>)}
              </select>
            </label>
          </div>
          <button className="primary-button">Add to backlog</button>
        </form>

        <div className="list-stack">
          {items.filter(item => item.status === 'Backlog').map(item => (
            <article className="panel backlog-item" key={item.id}>
              <div>
                <span className={`priority ${item.priority.toLowerCase()}`}>{item.priority}</span>
                <h3>{item.title}</h3>
                <p>{item.description}</p>
              </div>
              <strong>{item.storyPoints} points</strong>
            </article>
          ))}
        </div>
      </section>
    </>
  )
}
