use std::path::PathBuf;

use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(
    name = "sentinelhash",
    version,
    about = "Create file baselines and check directories for unexpected changes."
)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,
}

#[derive(Subcommand)]
pub enum Commands {
    /// Create a trusted baseline for a directory.
    Baseline {
        /// Directory that should be scanned.
        path: PathBuf,

        /// JSON file where the baseline will be stored.
        #[arg(short, long, default_value = "baseline.json")]
        output: PathBuf,

        /// File names, folder names or glob patterns to ignore.
        #[arg(short, long)]
        ignore: Vec<String>,
    },

    /// Compare a directory against an existing baseline.
    Check {
        /// Directory that should be checked.
        path: PathBuf,

        /// Baseline created by the baseline command.
        #[arg(short, long, default_value = "baseline.json")]
        baseline: PathBuf,

        /// Optional JSON file for the completed report.
        #[arg(short, long)]
        report: Option<PathBuf>,

        /// File names, folder names or glob patterns to ignore.
        #[arg(short, long)]
        ignore: Vec<String>,
    },
}
