# Matthew Uhlar · Software portfolio

I’m building small, useful applications with clear code, repeatable tests, and enough documentation to make them easy to run. This collection covers browser interfaces, API design, relational data, and developer tools.

## Start here

| Project | Stack | What to look at |
| --- | --- | --- |
| [Application Tracker](showcase/application-tracker/) | TypeScript, JavaScript, HTML, CSS | Validated application data, accessible forms, filtering, and local persistence |
| [Support Ticket API](showcase/support-ticket-api/) | Python, SQLite, SQL | HTTP endpoints, state transitions, transactions, and integration tests |
| [Dependency Lens](showcase/dependency-lens/) | JavaScript, Node.js | Import resolution, graph traversal, cycle detection, and a tested CLI |

Each project has its own setup instructions, examples, tests, and a short explanation of the tradeoffs I made. The commits separate the initial implementation, tests, and later improvements so the development process is easy to follow.

For a visual overview, open [the portfolio page](showcase/index.html) after cloning this repository. It is a static page with no build step.

## Run the collection

You’ll need Node.js 24 and Python 3.11 or newer. The showcase applications do not need third-party runtime packages.

```sh
git clone --filter=blob:none --sparse https://github.com/Matthew-Uhlar/Portfolio.git
cd Portfolio
git sparse-checkout set showcase .github
```

Use each project’s README for its start and test commands. The root GitHub Actions workflow runs the showcase checks on pushes and pull requests.

## Earlier work

[Major Projects](Major%20Projects/) and [Old](Old/) contain my earlier work. The `showcase` directory is the starting point for this collection; its checks are scoped to those projects.

## About this work

These are portfolio projects, not claims of production deployments or client work. I used AI assistance during development and review. The source, tests, and documented limitations are here so the implementation can be evaluated directly.
