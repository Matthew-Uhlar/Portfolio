# Enterprise Inventory & Asset Management System

This project is a full stack inventory management application that I built to demonstrate enterprise software development skills. The goal was to create something that looks and feels like a real business application instead of another tutorial project.

## Features

- Secure login with JWT authentication
- Role based permissions for administrators and staff
- Inventory and asset management
- Purchase request workflow
- Low inventory notifications
- Dashboard with inventory metrics
- REST API with Swagger
- PostgreSQL database
- Docker support
- React and TypeScript frontend
- ASP.NET Core backend

## Why I Built It

I wanted a project that demonstrates the same technologies and architecture used in many enterprise environments. Rather than focusing on a simple CRUD application I added authentication, user roles, reporting and approval workflows to better represent production software.

## Running the Project

```bash
docker compose up --build
```

Frontend:
http://localhost:5173

Swagger:
http://localhost:8080/swagger
