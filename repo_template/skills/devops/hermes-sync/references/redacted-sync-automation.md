# Redacted Sync Automation

This document outlines the pattern for performing a secure, automated backup of the Hermes configuration and skills.

## Prerequisites
- **GitHub Token**: A valid `GITHUB_TOKEN` must be present in `~/.hermes/.env`.
- **Sync Scripts**: The synchronization scripts (e.g., `sync_to_repo.py`, `hermes-sync-wrapper.py`) should be available in the environment.

## Execution Pattern
For automated environments (like cron jobs), use the wrapper script to ensure the correct sequence of redaction and synchronization:

```bash
python3 /path/to/hermes-sync-dev/scripts/hermes-sync-wrapper.py sync
```

## Redaction Logic
The `sync_to_repo.py` script performs deep redaction on the `config.yaml` file. It recursively scans the configuration dictionary and replaces any values associated with keys containing "key", "token", "secret", or "password" with `[REDACTED]`.

## Verification
After running the sync, verify:
1. The local repository state is clean: `git status`.
2. The redacted config exists in the repo: `cat <repo_path>/configs/config.yaml`.
3. The remote origin is correctly configured: `git remote -v`.
