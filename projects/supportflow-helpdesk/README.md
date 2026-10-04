# SupportFlow

[![SupportFlow demo](https://raw.githubusercontent.com/Matthew-Uhlar/Portfolio/main/demos/supportflow-helpdesk-demo.gif)](https://matthew-uhlar.github.io/Portfolio/demos/supportflow-helpdesk-demo.mp4)

**[Watch the full demo video (MP4)](https://matthew-uhlar.github.io/Portfolio/demos/supportflow-helpdesk-demo.mp4)** | An employee files a ticket in the React app, a technician finds it in the queue, assigns it, replies and adds an internal note, the employee sees the reply but never the note, then an admin checks the dashboard.

SupportFlow is a help desk and service request platform I built with Java and Spring Boot. I wanted a project that felt closer to the type of software a real company would use instead of another basic CRUD application.

The application gives employees a way to submit support tickets and gives support staff a structured workflow for assigning, prioritizing and resolving them. It has a React frontend for all three roles and a REST API you can also use directly. I also added authentication, role-based permissions, reporting and audit history so the project demonstrates more than basic API development.

## Main Features

- React frontend: dashboard, ticket queue with search and filters, ticket detail with conversation, internal notes and history
- JWT authentication
- Employee, technician and administrator roles
- Employees only see their own tickets, and internal technician notes are never sent to them
- Ticket creation and assignment
- Priority and status workflows
- Comments and internal updates
- Ticket history
- Dashboard reporting
- Search and filtering
- PostgreSQL database
- Swagger API documentation
- Docker support
- Unit tests with JUnit 5 and Mockito, run on every push by GitHub Actions

## Tech Stack

- Java 21
- Spring Boot 3
- Spring Security
- Spring Data JPA
- PostgreSQL
- JWT
- Maven
- Docker
- JUnit 5
- Mockito
- OpenAPI / Swagger
- React 18, TypeScript and Vite (frontend)

## Run With Docker

From the project folder run:

```bash
docker compose up --build
```

Then open:

- Application: http://localhost:5175
- API: http://localhost:8090
- Swagger: http://localhost:8090/swagger-ui.html

## Demo Accounts

Administrator:

```text
admin@example.com
Admin123!
```

Technician:

```text
tech@example.com
Tech123!
```

Employee:

```text
employee@example.com
Employee123!
```

## Run Locally

You will need Java 21 and PostgreSQL.

```bash
mvn spring-boot:run
```

In a second terminal, start the frontend (it proxies API calls to port 8090):

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5175.

## Run the Tests

```bash
mvn test
```

## Why I Built It

Java and Spring Boot show up in a lot of enterprise software roles. I built this project to demonstrate backend development, security, database design, testing and business workflow logic in one application.

## What I Would Add Next

- Email notifications
- File attachments
- Service level agreement tracking
- Redis caching
- WebSocket updates
- Azure or AWS deployment
