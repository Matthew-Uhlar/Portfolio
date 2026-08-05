# SentinelHash

SentinelHash is a file integrity monitoring tool I built in Rust. It creates a trusted baseline of files in a directory and later checks for anything that was added, changed or removed.

I wanted this project to show practical systems programming instead of another small command line demo. It works with real directories, hashes files in parallel, stores a baseline as JSON and generates clear reports that could be used for security monitoring or change control.

## Features

- Creates a baseline of files and SHA-256 hashes
- Detects added, modified and deleted files
- Scans files in parallel
- Supports ignored paths and file patterns
- Exports reports as JSON
- Shows a readable summary in the terminal
- Includes file size and modified time
- Handles inaccessible files without stopping the entire scan
- Includes unit and integration tests
- Runs on Windows, macOS and Linux

## Tech Used

- Rust
- Rayon
- SHA-256
- Serde
- Clap
- WalkDir
- JSON storage

## Why I Built It

File integrity monitoring is used in cybersecurity, compliance and system administration. I built this to demonstrate Rust, concurrency, error handling, file system access, hashing and structured data without relying on a web framework.

## Build

Install the current stable version of Rust from rustup.

```bash
cargo build --release
```

The compiled application will be in:

```text
target/release/sentinelhash
```

On Windows it will be:

```text
target\release\sentinelhash.exe
```

## Usage

### Create a baseline

```bash
cargo run -- baseline ./example-data --output baseline.json
```

### Check for changes

```bash
cargo run -- check ./example-data --baseline baseline.json
```

### Save the report

```bash
cargo run -- check ./example-data --baseline baseline.json --report report.json
```

### Ignore files or folders

```bash
cargo run -- baseline ./example-data --output baseline.json --ignore target --ignore "*.log"
```

## Example Output

```text
Scan complete

Files checked: 24
Added:         1
Modified:      2
Deleted:       0
Errors:        0

ADDED
  notes/new-file.txt

MODIFIED
  config/settings.json
  src/main.rs
```

## Testing

```bash
cargo test
```

## Project Structure

```text
src/
  main.rs
  cli.rs
  models.rs
  scanner.rs
  storage.rs
  report.rs
tests/
  integrity_scan.rs
```

## What I Would Add Next

- Continuous directory watching
- Signed baseline files
- Email or webhook alerts
- SQLite history
- Config files
- Scheduled scans
- A small web dashboard
