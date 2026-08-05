use std::{fs, path::Path};

use anyhow::{Context, Result};

use crate::models::{IntegrityReport, ScanResult};

pub fn save_baseline(path: &Path, scan: &ScanResult) -> Result<()> {
    let json = serde_json::to_string_pretty(scan)?;
    fs::write(path, json)
        .with_context(|| format!("The baseline could not be saved to {}", path.display()))?;

    Ok(())
}

pub fn load_baseline(path: &Path) -> Result<ScanResult> {
    let json = fs::read_to_string(path)
        .with_context(|| format!("The baseline could not be opened: {}", path.display()))?;

    serde_json::from_str(&json)
        .with_context(|| format!("The baseline is not valid JSON: {}", path.display()))
}

pub fn save_report(path: &Path, report: &IntegrityReport) -> Result<()> {
    let json = serde_json::to_string_pretty(report)?;
    fs::write(path, json)
        .with_context(|| format!("The report could not be saved to {}", path.display()))?;

    Ok(())
}
