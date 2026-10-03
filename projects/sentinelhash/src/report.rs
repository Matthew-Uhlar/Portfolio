use crate::models::{FileChange, IntegrityReport, ScanResult};

pub fn build_report(baseline: &ScanResult, current: &ScanResult) -> IntegrityReport {
    let mut added = Vec::new();
    let mut modified = Vec::new();
    let mut deleted = Vec::new();

    for (path, current_file) in &current.files {
        match baseline.files.get(path) {
            None => added.push(current_file.clone()),
            Some(saved_file) if saved_file.sha256 != current_file.sha256 => {
                modified.push(FileChange {
                    path: path.clone(),
                    before: saved_file.clone(),
                    after: current_file.clone(),
                });
            }
            _ => {}
        }
    }

    for (path, saved_file) in &baseline.files {
        if !current.files.contains_key(path) {
            deleted.push(saved_file.clone());
        }
    }

    added.sort_by(|left, right| left.path.cmp(&right.path));
    modified.sort_by(|left, right| left.path.cmp(&right.path));
    deleted.sort_by(|left, right| left.path.cmp(&right.path));

    IntegrityReport {
        baseline_root: baseline.root.clone(),
        checked_at: current.scanned_at,
        files_checked: current.files.len(),
        added,
        modified,
        deleted,
        errors: current.errors.clone(),
    }
}

pub fn print_report(report: &IntegrityReport) {
    println!("Scan complete");
    println!();
    println!("Files checked: {}", report.files_checked);
    println!("Added:         {}", report.added.len());
    println!("Modified:      {}", report.modified.len());
    println!("Deleted:       {}", report.deleted.len());
    println!("Errors:        {}", report.errors.len());

    print_section(
        "ADDED",
        report.added.iter().map(|file| file.path.as_str()),
    );

    print_section(
        "MODIFIED",
        report.modified.iter().map(|change| change.path.as_str()),
    );

    print_section(
        "DELETED",
        report.deleted.iter().map(|file| file.path.as_str()),
    );

    if !report.errors.is_empty() {
        println!();
        println!("ERRORS");

        for error in &report.errors {
            println!("  {}: {}", error.path, error.message);
        }
    }

    if !report.has_changes() && report.errors.is_empty() {
        println!();
        println!("No unexpected changes were found.");
    }
}

fn print_section<'a>(title: &str, paths: impl Iterator<Item = &'a str>) {
    let values: Vec<&str> = paths.collect();

    if values.is_empty() {
        return;
    }

    println!();
    println!("{title}");

    for path in values {
        println!("  {path}");
    }
}

#[cfg(test)]
mod tests {
    use std::collections::BTreeMap;

    use chrono::Utc;

    use super::*;
    use crate::models::{FileRecord, ScanResult};

    fn file(path: &str, hash: &str) -> FileRecord {
        FileRecord {
            path: path.to_string(),
            sha256: hash.to_string(),
            size_bytes: 10,
            modified_at: None,
        }
    }

    fn scan(files: Vec<FileRecord>) -> ScanResult {
        let files = files
            .into_iter()
            .map(|file| (file.path.clone(), file))
            .collect::<BTreeMap<_, _>>();

        ScanResult {
            root: "test".to_string(),
            scanned_at: Utc::now(),
            files,
            errors: vec![],
        }
    }

    #[test]
    fn report_detects_added_modified_and_deleted_files() {
        let baseline = scan(vec![
            file("same.txt", "111"),
            file("changed.txt", "222"),
            file("deleted.txt", "333"),
        ]);

        let current = scan(vec![
            file("same.txt", "111"),
            file("changed.txt", "999"),
            file("added.txt", "444"),
        ]);

        let report = build_report(&baseline, &current);

        assert_eq!(report.added.len(), 1);
        assert_eq!(report.modified.len(), 1);
        assert_eq!(report.deleted.len(), 1);
    }
}
