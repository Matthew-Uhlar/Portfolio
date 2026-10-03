mod cli;
mod models;
mod report;
mod scanner;
mod storage;

use anyhow::Result;
use clap::Parser;

use crate::cli::{Cli, Commands};
use crate::report::{build_report, print_report};
use crate::scanner::{scan_directory, ScanOptions};
use crate::storage::{load_baseline, save_baseline, save_report};

fn main() {
    if let Err(error) = run() {
        eprintln!("SentinelHash could not finish the scan: {error}");
        std::process::exit(1);
    }
}

fn run() -> Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Commands::Baseline {
            path,
            output,
            ignore,
        } => {
            let options = ScanOptions::new(path, ignore)?;
            let scan = scan_directory(&options)?;

            save_baseline(&output, &scan)?;

            println!("Baseline created");
            println!("Files recorded: {}", scan.files.len());
            println!("Errors:         {}", scan.errors.len());
            println!("Saved to:       {}", output.display());
        }
        Commands::Check {
            path,
            baseline,
            report,
            ignore,
        } => {
            let saved = load_baseline(&baseline)?;
            let options = ScanOptions::new(path, ignore)?;
            let current = scan_directory(&options)?;
            let integrity_report = build_report(&saved, &current);

            print_report(&integrity_report);

            if let Some(report_path) = report {
                save_report(&report_path, &integrity_report)?;
                println!();
                println!("Report saved to {}", report_path.display());
            }

            if integrity_report.has_changes() {
                std::process::exit(2);
            }
        }
    }

    Ok(())
}
