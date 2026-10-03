import type { Incident } from '../types'

export default function IncidentMap({ incidents }: { incidents: Incident[] }) {
  return (
    <div className="map-panel">
      <div className="map-grid" />
      {incidents.slice(0, 8).map((incident, index) => (
        <div
          key={incident.id}
          className={`map-marker ${incident.severity.toLowerCase()}`}
          style={{
            left: `${14 + ((index * 19) % 72)}%`,
            top: `${18 + ((index * 23) % 60)}%`
          }}
          title={`${incident.title} at ${incident.address}`}
        >
          {incident.id}
        </div>
      ))}

      <div className="map-caption">
        <strong>Map-ready incident view</strong>
        <span>Coordinates are stored for each incident. Connect Google Maps or Azure Maps for live plotting.</span>
      </div>
    </div>
  )
}
