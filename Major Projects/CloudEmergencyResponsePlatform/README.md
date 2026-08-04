# Cloud-Based Emergency Response Platform

I built this project to show how a real-time response system could help emergency teams manage incidents, assign resources and keep information in one place. The goal was to create something practical that connects software development with mapping, live updates and operational decision-making.

The application lets dispatchers create incidents, update severity, assign available response units and view activity from a live dashboard. It also includes a map-ready structure so location data can be displayed with Google Maps or Azure Maps later.

## Main Features

- Secure JWT login
- Dispatcher and responder roles
- Incident creation and status tracking
- Resource and vehicle assignment
- Live updates with SignalR
- Incident timeline and activity log
- Dashboard metrics
- Location coordinates for map integration
- REST API with Swagger
- PostgreSQL database
- Docker support
- React and TypeScript frontend
- ASP.NET Core backend

## Tech Stack

### Backend
- C#
- ASP.NET Core 8
- Entity Framework Core
- SignalR
- PostgreSQL
- JWT authentication

### Frontend
- React
- TypeScript
- Vite
- CSS

## Run It With Docker

From the project folder run:

```bash
docker compose up --build
```

Then open:

- Application: http://localhost:5174
- Swagger: http://localhost:8081/swagger

## Demo Accounts

Dispatcher:

```text
dispatcher@example.com
Dispatch123!
```

Responder:

```text
responder@example.com
Responder123!
```

## Map Integration

The frontend includes latitude and longitude fields and the backend stores both values on each incident. The map area currently uses a lightweight visual placeholder so the project runs without a paid API key.

To connect a real map provider later:

1. Add a Google Maps or Azure Maps key.
2. Replace the placeholder in `IncidentMap.tsx`.
3. Plot each incident by latitude and longitude.
4. Add routing or travel time estimates for assigned units.

## Portfolio Notes

This is an MVP. In a production version I would also add:

- Push notifications
- Mobile offline support
- Route optimization
- File and photo uploads
- Emergency service integrations
- Audit export
- Automated tests
- Azure deployment
- GitHub Actions CI/CD
