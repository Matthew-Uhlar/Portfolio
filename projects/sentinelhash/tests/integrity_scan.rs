use std::fs;

use sentinelhash::{models::ScanResult, report::build_report, scanner::{scan_directory, ScanOptions}};
use tempfile::tempdir;

#[test]
fn full_scan_detects_a_changed_file() {
    let directory = tempdir().unwrap();
    let file_path = directory.path().join("config.txt");

    fs::write(&file_path, "version one").unwrap();

    let options = ScanOptions::new(directory.path().to_path_buf(), vec![]).unwrap();
    let baseline: ScanResult = scan_directory(&options).unwrap();

    fs::write(&file_path, "version two").unwrap();

    let current = scan_directory(&options).unwrap();
    let report = build_report(&baseline, &current);

    assert_eq!(report.modified.len(), 1);
    assert_eq!(report.modified[0].path, "config.txt");
}
