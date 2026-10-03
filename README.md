# Matthew Uhlar | Software Portfolio

**[Live portfolio site with demo videos](https://matthew-uhlar.github.io/Portfolio/)** | [LinkedIn](https://www.linkedin.com/in/matthew-uhlar-ssm-92623617a) | [GitHub profile](https://github.com/Matthew-Uhlar)

Software developer in Austin, TX (open to remote) with a BS in Computer Science and an MS in AI and Machine Learning in progress. I build full stack applications with C# and ASP.NET Core, Java and Spring Boot and React with TypeScript on PostgreSQL. Every project below has a recorded demo so you can see it working before you clone anything.

## Featured projects

| Project | What it is | Stack | Demo |
| --- | --- | --- | --- |
| [Project Pilot: AI Project Management Assistant](projects/ai-project-management-assistant/) | Agile planning tool with a Kanban board and an AI assistant that drafts stories, points, risks and sprint summaries | C#, ASP.NET Core 8, EF Core, React, TypeScript, PostgreSQL, Docker | [Video](https://matthew-uhlar.github.io/Portfolio/demos/ai-project-management-assistant-demo.mp4) |
| [SupportFlow Help Desk API](projects/supportflow-helpdesk/) | Ticketing API with roles, status workflows, comments, audit history and reporting | Java 21, Spring Boot 3, Spring Security, JPA, PostgreSQL, JUnit 5 | [Video](https://matthew-uhlar.github.io/Portfolio/demos/supportflow-helpdesk-demo.mp4) |
| [Response Grid: Emergency Response Platform](projects/emergency-response-platform/) | Real-time dispatch app with live updates over SignalR | C#, ASP.NET Core 8, SignalR, React, PostgreSQL, Docker | [Video](https://matthew-uhlar.github.io/Portfolio/demos/emergency-response-platform-demo.mp4) |
| [SignalReady](https://github.com/Matthew-Uhlar/signalready) | Predictive maintenance modeling studio (ABB Accelerator Hackathon 2026) | Python, scikit-learn, pandas, Streamlit | [Video](https://matthew-uhlar.github.io/Portfolio/demos/signalready-demo.mp4) |
| [StockPilot: Enterprise Inventory System](projects/enterprise-inventory-system/) | Inventory, asset tracking and purchase request approvals | C#, ASP.NET Core 8, React, TypeScript, PostgreSQL, Docker | [Video](https://matthew-uhlar.github.io/Portfolio/demos/enterprise-inventory-system-demo.mp4) |
| [SentinelHash](projects/sentinelhash/) | File integrity monitor that catches added, modified and deleted files | Rust, Rayon, Serde, Clap | [Video](https://matthew-uhlar.github.io/Portfolio/demos/sentinelhash-demo.mp4) |

## More projects

| Project | What it is | Stack | Demo |
| --- | --- | --- | --- |
| [Childcare Inventory System](projects/childcare-inventory-system/) | Supply tracking and request approvals for a childcare center | Python, Flask, SQLite | [Video](https://matthew-uhlar.github.io/Portfolio/demos/childcare-inventory-demo.mp4) |
| [Signal Siege](projects/signal-siege/) | Wave survival game with all graphics drawn in code | Python, Pygame | [Video](https://matthew-uhlar.github.io/Portfolio/demos/signal-siege-demo.mp4) |
| [Prestige Construction website](projects/prestige-construction-website/) | Marketing site for a Colorado general contractor | HTML, CSS, JavaScript, PHP | [Video](https://matthew-uhlar.github.io/Portfolio/demos/prestige-construction-demo.mp4) |
| [Application Tracker](showcase/application-tracker/) | Job search pipeline with validated JSON backups | TypeScript, Node.js | [Video](https://matthew-uhlar.github.io/Portfolio/demos/application-tracker-demo.mp4) |
| [Support Ticket API](showcase/support-ticket-api/) | Standard-library API with SQLite transactions and integration tests | Python, SQLite | [Video](https://matthew-uhlar.github.io/Portfolio/demos/support-ticket-api-demo.mp4) |
| [Dependency Lens](showcase/dependency-lens/) | CLI that maps JS/TS imports and finds cycles | JavaScript, Node.js | [Video](https://matthew-uhlar.github.io/Portfolio/demos/dependency-lens-demo.mp4) |
| [CSC500 Shopping Cart](https://github.com/Matthew-Uhlar/CSC500-Portfolio) | Object-oriented Python final project | Python | [Video](https://matthew-uhlar.github.io/Portfolio/demos/csc500-shopping-cart-demo.mp4) |

## Repository layout

```text
projects/   full applications, each with its own README, Docker setup where relevant and demo
showcase/   smaller focused projects with tests run by GitHub Actions, plus the portfolio website
demos/      recorded demo videos (MP4) and previews (GIF)
archive/    earlier coursework and older projects, kept for reference
```

Demos are recorded by the [Record project demos](.github/workflows/record-demos.yml) workflow. It builds each app (Docker Compose for the full stack ones), drives it with a scripted Playwright browser or terminal session and commits the video, so every demo shows the code in this repository actually running.

## About this work

These are portfolio projects rather than claims of production deployments. I used AI assistance during development and review. The source, tests and documented limitations are here so the work can be evaluated directly.
