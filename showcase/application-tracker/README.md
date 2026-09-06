# Application Tracker

A small browser app for keeping a job search organized: save roles, move them through a pipeline, and keep follow-up notes in one place.

I wanted the core workflow to feel straightforward. The app starts empty, keeps data in the browser, and uses JSON backups so moving data doesn't depend on an account or a service staying online.

## Run locally

Install Node.js 24 or later, then from the portfolio repository:

```sh
cd showcase/application-tracker
npm start
```

Open http://127.0.0.1:3000. No package installation is needed. If you're running a standalone copy, start inside this project directory instead. Set the `PORT` environment variable to use a different port; browser storage is separate for each origin, including the port.

## What it does

- Create, edit, and delete applications with company, role, posting URL, and notes.
- Change status between Saved, Applied, Interview, Offer, and Closed. Moving backward is allowed because real hiring processes aren't always linear.
- Search company, role, and notes; filter by status; see totals for the full collection.
- Export versioned JSON backups and import them after validation. Import replaces the collection after a confirmation.
- Keep multiple tabs up to date through browser storage events.

## How it's built

`src/applications.ts` holds the typed domain model, runtime validation, filtering, and counts. `server.mjs` uses Node's built-in TypeScript stripping to serve that same module to the browser as JavaScript. This avoids maintaining two versions of the validation rules. Type stripping is not type checking; a separate strict TypeScript check validates the domain module during development. There are no runtime dependencies.

The frontend uses browser APIs, semantic HTML, labeled controls, a native modal dialog, and text nodes for user content. Posting links only accept HTTP or HTTPS. The local server serves four explicitly listed paths, binds to loopback, and sets a restrictive content security policy.

## Checks

```sh
npm ci
npm run check
npm test
```

TypeScript is a development dependency; install it with `npm ci` before running the type check. Starting the app and running runtime tests still work without installing packages.

Tests cover field validation, unsafe URLs, duplicate IDs, malformed backups, the import size limit, search, ordering, counts, asset delivery, browser-ready domain code, and blocked server paths. The portfolio's root workflow runs these tests.

For a manual browser check, create a role, edit its status, search for a word in its notes, reload, export a backup, delete the role, then import the backup. Try an invalid backup and verify the existing collection stays intact. Check the form with a keyboard and at a narrow window width.

## Tradeoffs

This is a local portfolio project, not a hosted recruiting system. There is no authentication, server database, cloud sync, or automatic backup. Clearing site data removes the collection. Up to 1,000 applications and 10 MB backup files are supported. Storage write failures leave the current in-memory collection unchanged. Corrupt saved data blocks writes rather than silently replacing it.

Multiple tabs use last-write-wins storage; simultaneous edits can overwrite each other. Notes are plain text. Browser automation and screen-reader testing aren't included in the current test suite.

Useful next steps would be optional reminders, merging imports with a conflict preview, and browser tests for the full backup round trip.

## License

MIT. See [LICENSE](LICENSE).
