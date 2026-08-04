import { FormEvent, useEffect, useState } from 'react'
import { api } from '../api'
import { useProject } from '../hooks'
import type { Sprint } from '../types'

type GeneratedStory = {
  title: string
  description: string
  acceptanceCriteria: string
  priority: string
  suggestedPoints: number
}

type StoryResponse = {
  overview: string
  stories: GeneratedStory[]
}

type RiskResponse = {
  overallRisk: string
  risks: string[]
  recommendations: string[]
}

type SummaryResponse = {
  summary: string
  highlights: string[]
  nextSteps: string[]
}

export default function Assistant() {
  const { project } = useProject()
  const [idea, setIdea] = useState('')
  const [stories, setStories] = useState<StoryResponse | null>(null)
  const [risk, setRisk] = useState<RiskResponse | null>(null)
  const [summary, setSummary] = useState<SummaryResponse | null>(null)
  const [sprint, setSprint] = useState<Sprint | null>(null)
  const [busy, setBusy] = useState('')

  useEffect(() => {
    if (project) {
      api<Sprint[]>(`/sprints/project/${project.id}`)
        .then(values => setSprint(values.find(value => value.isActive) ?? values[0] ?? null))
    }
  }, [project])

  async function generate(event: FormEvent) {
    event.preventDefault()
    if (!project) return
    setBusy('stories')
    try {
      setStories(await api<StoryResponse>('/ai/generate-stories', {
        method: 'POST',
        body: JSON.stringify({ projectId: project.id, featureIdea: idea })
      }))
    } finally {
      setBusy('')
    }
  }

  async function reviewRisk() {
    if (!project) return
    setBusy('risk')
    try {
      setRisk(await api<RiskResponse>('/ai/risk-review', {
        method: 'POST',
        body: JSON.stringify({ projectId: project.id })
      }))
    } finally {
      setBusy('')
    }
  }

  async function summarize() {
    if (!sprint) return
    setBusy('summary')
    try {
      setSummary(await api<SummaryResponse>('/ai/sprint-summary', {
        method: 'POST',
        body: JSON.stringify({ sprintId: sprint.id })
      }))
    } finally {
      setBusy('')
    }
  }

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">Planning support</span>
          <h2>AI Assistant</h2>
          <p>Use the assistant for repetitive planning work while the team keeps control of the final decisions.</p>
        </div>
      </header>

      <section className="assistant-grid">
        <article className="panel">
          <h3>Turn an idea into user stories</h3>
          <p className="muted">Describe a feature in plain language and the assistant will break it into a practical first set of stories.</p>
          <form className="form-stack" onSubmit={generate}>
            <textarea
              rows={5}
              value={idea}
              onChange={event => setIdea(event.target.value)}
              placeholder="Example: Let staff scan a QR code to update inventory from a phone"
              required
            />
            <button className="primary-button" disabled={busy === 'stories'}>
              {busy === 'stories' ? 'Working on it...' : 'Generate stories'}
            </button>
          </form>
        </article>

        <article className="panel">
          <h3>Review project risk</h3>
          <p className="muted">Check the backlog for large work, missing owners and other planning issues.</p>
          <button className="secondary-button" onClick={reviewRisk} disabled={busy === 'risk'}>
            {busy === 'risk' ? 'Reviewing...' : 'Run risk review'}
          </button>
          {risk && (
            <div className="result-block">
              <strong>Overall risk: {risk.overallRisk}</strong>
              <h4>What stands out</h4>
              <ul>{risk.risks.map(value => <li key={value}>{value}</li>)}</ul>
              <h4>Recommended next steps</h4>
              <ul>{risk.recommendations.map(value => <li key={value}>{value}</li>)}</ul>
            </div>
          )}
        </article>

        <article className="panel">
          <h3>Summarize the active sprint</h3>
          <p className="muted">Create a quick status update from the current sprint data.</p>
          <button className="secondary-button" onClick={summarize} disabled={!sprint || busy === 'summary'}>
            {busy === 'summary' ? 'Summarizing...' : 'Create sprint summary'}
          </button>
          {summary && (
            <div className="result-block">
              <p>{summary.summary}</p>
              <h4>Highlights</h4>
              <ul>{summary.highlights.map(value => <li key={value}>{value}</li>)}</ul>
              <h4>Next steps</h4>
              <ul>{summary.nextSteps.map(value => <li key={value}>{value}</li>)}</ul>
            </div>
          )}
        </article>
      </section>

      {stories && (
        <section className="generated-section">
          <div className="panel">
            <span className="eyebrow">Generated plan</span>
            <p>{stories.overview}</p>
          </div>
          <div className="story-grid">
            {stories.stories.map(story => (
              <article className="panel" key={story.title}>
                <div className="card-topline">
                  <span className={`priority ${story.priority.toLowerCase()}`}>{story.priority}</span>
                  <strong>{story.suggestedPoints} pts</strong>
                </div>
                <h3>{story.title}</h3>
                <p>{story.description}</p>
                <h4>Acceptance criteria</h4>
                <p>{story.acceptanceCriteria}</p>
              </article>
            ))}
          </div>
        </section>
      )}
    </>
  )
}
