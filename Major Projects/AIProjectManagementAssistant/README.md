# AI Project Management Assistant

I built this project to combine my software development background with the project management and Agile work I have done. The application gives a team one place to manage projects, organize a backlog, move work through a board and use an AI assistant for some of the repetitive planning work.

The AI features are intentionally practical. It can turn a rough feature idea into user stories, suggest story points, summarize a sprint and point out common project risks. The project runs with a built-in local assistant by default, so it works without a paid API key. The backend was also structured so another AI provider can be added later without changing the rest of the application.

## Main Features

- JWT login and role-based access
- Project and sprint management
- Backlog with priorities and story points
- Kanban board with drag and drop
- AI user story generator
- AI story point suggestion
- AI sprint summary
- AI risk review
- Dashboard metrics
- PostgreSQL database
- Swagger API documentation
- Docker support

## Tech Stack

### Backend
- C#
- ASP.NET Core 8
- Entity Framework Core
- PostgreSQL
- JWT authentication

### Frontend
- React
- TypeScript
- Vite
- CSS

## Run It With Docker

From the main project folder run:

```bash
docker compose up --build
```

Then open:

- Application: http://localhost:5173
- Swagger: http://localhost:8080/swagger

## Demo Accounts

Administrator:

```text
admin@example.com
Admin123!
```

Team member:

```text
member@example.com
Member123!
```

## How the AI Part Works

The default assistant uses the project data and a set of planning rules to create useful responses locally. I chose this approach so anyone reviewing the project can run every feature without setting up a third-party account.

The `IAiPlanningService` interface keeps the AI logic separate from the controllers. A hosted AI provider can be added later by creating another implementation and registering it in `Program.cs`.

## Portfolio Notes

This is an MVP and there are several areas I would expand in a production version:

- Add refresh tokens and account management
- Add automated tests
- Add real-time board updates with SignalR
- Add file attachments and comments
- Add email or Slack notifications
- Deploy the frontend and API to Azure
- Add GitHub Actions for CI/CD
