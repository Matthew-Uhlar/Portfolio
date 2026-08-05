# SupportFlow

SupportFlow is a help desk and service request platform I built with Java and Spring Boot. I wanted a project that felt closer to the type of software a real company would use instead of another basic CRUD application.

The application gives employees a way to submit support tickets and gives support staff a structured workflow for assigning, prioritizing and resolving them. I also added authentication, role-based permissions, reporting and audit history so the project demonstrates more than basic API development.

## Main Features

- JWT authentication
- Employee, technician and administrator roles
- Ticket creation and assignment
- Priority and status workflows
- Comments and internal updates
- Ticket history
- Dashboard reporting
- Search and filtering
- PostgreSQL database
- Swagger API documentation
- Docker support
- Unit and integration tests

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

## Run With Docker

From the project folder run:

```bash
docker compose up --build
```

Then open:

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

## Why I Built It

Java and Spring Boot show up in a lot of enterprise software roles. I built this project to demonstrate backend development, security, database design, testing and business workflow logic in one application.

## What I Would Add Next

- Email notifications
- File attachments
- Service level agreement tracking
- Redis caching
- WebSocket updates
- React frontend
- Azure or AWS deployment
- GitHub Actions
