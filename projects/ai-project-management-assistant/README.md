# AI Project Management Assistant

[![AI Project Management Assistant demo](https://raw.githubusercontent.com/Matthew-Uhlar/Portfolio/main/demos/ai-project-management-assistant-demo.gif)](https://matthew-uhlar.github.io/Portfolio/demos/ai-project-management-assistant-demo.mp4)

**[Watch the full demo video (MP4)](https://matthew-uhlar.github.io/Portfolio/demos/ai-project-management-assistant-demo.mp4)** | Sign in, move work across the sprint board with drag and drop, add a backlog item, then have the AI assistant generate user stories, review risk and summarize the sprint.

I built this project to combine my software development background with the project management and Agile work I have done. The application gives a team one place to manage projects, organize a backlog, move work through a board and use an AI assistant for some of the repetitive planning work.

The AI features are intentionally practical. It can turn a rough feature idea into user stories, suggest story points, summarize a sprint and point out common project risks. With an Anthropic API key the assistant answers using Claude. Without one it uses a built-in rules engine, so every feature works with no paid account.

## Main Features

- JWT login and role-based access
- Project and sprint management
- Backlog with priorities and story points
- Kanban board with drag and drop
- AI user story generator
- AI story point suggestion
- AI sprint summary
- AI risk review, powered by Claude when an API key is set
- Dashboard metrics
- PostgreSQL database
- Swagger API documentation
- Docker support
- xUnit tests and GitHub Actions CI
- One-command deployment to Azure Container Apps

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

Controllers only talk to the `IAiPlanningService` interface, which has two implementations:

- `ClaudeAiPlanningService` sends the project, sprint and backlog details to Anthropic's Messages API and asks for JSON in the exact shape the frontend uses. Replies are validated (story points snap to the Fibonacci scale, risk levels must be Low, Medium or High) before they reach the UI.
- `LocalAiPlanningService` is a rules engine that needs no account. It is the default, and the Claude service falls back to it whenever the API is unavailable, slow or returns something unusable, so the assistant never breaks the app.

The Assistant page shows which engine answered. To use Claude with Docker:

```bash
export ANTHROPIC_API_KEY=your-key
docker compose up --build
```

`Ai__Model` (or `ANTHROPIC_MODEL` with Docker Compose) picks the model and defaults to `claude-haiku-4-5`.

## Tests

```bash
dotnet test backend/ProjectAssistant.Api.Tests
```

The tests cover the rules engine, the Claude integration (with a fake HTTP handler, including the fallback paths) and password hashing. GitHub Actions runs them on every push.

## Deploy to Azure

See [deploy/azure](deploy/azure/README.md). One script creates the Container Apps environment, the PostgreSQL database and both apps, then prints a public URL with demo logins.

## Portfolio Notes

This is an MVP and there are several areas I would expand in a production version:

- Add refresh tokens and account management
- Add integration tests against a real PostgreSQL container
- Add real-time board updates with SignalR
- Add file attachments and comments
- Add email or Slack notifications
