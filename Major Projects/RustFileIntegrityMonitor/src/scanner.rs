use std::{
    collections::BTreeMap,
    fs::File,
    io::{BufReader, Read},
    path::{Path, PathBuf},
    time::SystemTime,
};

use anyhow::{bail, Context, Result};
use chrono::{DateTime, Utc};
use globset::{Glob, GlobSet, GlobSetBuilder};
use rayon::prelude::*;
use sha2::{Digest, Sha256};
use walkdir::WalkDir;

use crate::models::{FileRecord, ScanError, ScanResult};

pub struct ScanOptions {
    pub root: PathBuf,
    ignore_set: GlobSet,
    ignore_terms: Vec<String>,
}

impl ScanOptions {
    pub fn new(root: PathBuf, ignore_patterns: Vec<String>) -> Result<Self> {
        if !root.exists() {
            bail!("The directory does not exist: {}", root.display());
        }

        if !root.is_dir() {
            bail!("The scan path must be a directory: {}", root.display());
        }

        let mut builder = GlobSetBuilder::new();

        for pattern in &ignore_patterns {
            if pattern.contains('*') || pattern.contains('?') || pattern.contains('[') {
                builder.add(
                    Glob::new(pattern)
                        .with_context(|| format!("The ignore pattern is not valid: {pattern}"))?,
                );
            }
        }

        Ok(Self {
            root,
            ignore_set: builder.build()?,
            ignore_terms: ignore_patterns,
        })
    }

    fn should_ignore(&self, relative_path: &Path) -> bool {
        let normalized = normalize_path(relative_path);

        if self.ignore_set.is_match(&normalized) {
            return true;
        }

        relative_path.components().any(|component| {
            let value = component.as_os_str().to_string_lossy();
            self.ignore_terms.iter().any(|term| {
                !term.contains('*')
                    && !term.contains('?')
                    && !term.contains('[')
                    && value.eq_ignore_ascii_case(term)
            })
        })
    }
}

pub fn scan_directory(options: &ScanOptions) -> Result<ScanResult> {
    let root = options.root.canonicalize().with_context(|| {
        format!("The scan path could not be opened: {}", options.root.display())
    })?;

    let paths: Vec<PathBuf> = WalkDir::new(&root)
        .follow_links(false)
        .into_iter()
        .filter_map(|entry| match entry {
            Ok(entry) if entry.file_type().is_file() => {
                let relative = entry.path().strip_prefix(&root).ok()?;

                if options.should_ignore(relative) {
                    None
                } else {
                    Some(entry.path().to_path_buf())
                }
            }
            _ => None,
        })
        .collect();

    // Hashing is the slowest part of the scan so each file is handled in parallel.
    let results: Vec<Result<FileRecord, ScanError>> = paths
        .par_iter()
        .map(|path| scan_file(&root, path))
        .collect();

    let mut files = BTreeMap::new();
    let mut errors = Vec::new();

    for result in results {
        match result {
            Ok(record) => {
                files.insert(record.path.clone(), record);
            }
            Err(error) => errors.push(error),
        }
    }

    errors.sort_by(|left, right| left.path.cmp(&right.path));

    Ok(ScanResult {
        root: normalize_path(&root),
        scanned_at: Utc::now(),
        files,
        errors,
    })
}

fn scan_file(root: &Path, path: &Path) -> Result<FileRecord, ScanError> {
    let relative = path
        .strip_prefix(root)
        .map(normalize_path)
        .unwrap_or_else(|_| normalize_path(path));

    let metadata = path.metadata().map_err(|error| ScanError {
        path: relative.clone(),
        message: format!("Could not read file information: {error}"),
    })?;

    let hash = hash_file(path).map_err(|error| ScanError {
        path: relative.clone(),
        message: format!("Could not hash the file: {error}"),
    })?;

    let modified_at = metadata
        .modified()
        .ok()
        .and_then(system_time_to_utc);

    Ok(FileRecord {
        path: relative,
        sha256: hash,
        size_bytes: metadata.len(),
        modified_at,
    })
}

fn hash_file(path: &Path) -> Result<String> {
    let file = File::open(path)?;
    let mut reader = BufReader::new(file);
    let mut hasher = Sha256::new();
    let mut buffer = [0_u8; 64 * 1024];

    loop {
        let bytes_read = reader.read(&mut buffer)?;

        if bytes_read == 0 {
            break;
        }

        hasher.update(&buffer[..bytes_read]);
    }

    Ok(hex::encode(hasher.finalize()))
}

fn system_time_to_utc(value: SystemTime) -> Option<DateTime<Utc>> {
    Some(DateTime::<Utc>::from(value))
}

fn normalize_path(path: &Path) -> String {
    path.to_string_lossy().replace('\\', "/")
}

#[cfg(test)]
mod tests {
    use std::fs;

    use tempfile::tempdir;

    use super::*;

    #[test]
    fn scan_finds_files_and_creates_hashes() {
        let directory = tempdir().unwrap();
        fs::write(directory.path().join("notes.txt"), "hello world").unwrap();

        let options = ScanOptions::new(directory.path().to_path_buf(), vec![]).unwrap();
        let result = scan_directory(&options).unwrap();

        assert_eq!(result.files.len(), 1);
        assert!(result.files["notes.txt"].sha256.len() == 64);
    }

    #[test]
    fn scan_skips_ignored_folders() {
        let directory = tempdir().unwrap();
        fs::create_dir(directory.path().join("target")).unwrap();
        fs::write(directory.path().join("target/output.txt"), "skip me").unwrap();
        fs::write(directory.path().join("keep.txt"), "keep me").unwrap();

        let options = ScanOptions::new(
            directory.path().to_path_buf(),
            vec!["target".to_string()],
        )
        .unwrap();

        let result = scan_directory(&options).unwrap();

        assert_eq!(result.files.len(), 1);
        assert!(result.files.contains_key("keep.txt"));
    }
}
