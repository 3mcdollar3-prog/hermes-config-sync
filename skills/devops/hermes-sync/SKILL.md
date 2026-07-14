---
name: hermes-sync
description: "Manage Hermes configuration, skills, and cron jobs across multiple servers using a Git-based Infrastructure as Code approach."
version: 1.0.1
author: Hermes Agent
license: MIT
---

# Hermes Sync
Manage Hermes configuration, skills, and cron jobs across multiple servers using a Git-based "Infrastructure as Code" approach.

## Overview
Provides tools to back up your current Hermes state to a Git repository and deploy that state to other servers, ensuring fleet-wide consistency.

## Commands
- `sync`: Collects, redacts, and pushes the current state to the configured Git repository.
- `deploy <repo_path>`: Pulls the latest state from the Git repository and applies it to the local Hermes instance.

## Key Concepts
- **Redaction:** All sensitive information (API keys, tokens) is automatically stripped during the sync process.
- **Fleet Management:** Enables "one-click" updates across multiple servers by treating configuration as versioned code.
- **Git-Native Workflow:** Can be fully automated using a GitHub Personal Access Token (PAT) for autonomous pulls and pushes.

## Support Files
- `references/git-native-workflow.md`: Detailed documentation on the autonomous Git-native workflow.
- `references/redacted-sync-automation.md`: Documentation on performing secure, automated backups.

## Pitfalls
- **Malformed Remote URLs:** Ensure the Git remote URL in the repository template is a clean HTTPS URL (e.g., `https://github.com/user/repo.git`) and does *not* contain pre-baked authentication tokens. Hardcoded tokens in `.git/config` can cause "Bad hostname" errors during automated pushes. Additionally, in non-interactive environments, git may fail with "could not read Username/Password" because it cannot prompt for credentials. To resolve this, use `gh auth token` to retrieve the current session token and inject it dynamically into the remote URL (e.g., `git remote set-url origin "https://$(gh auth token)@github.com/user/repo.git"`) before pushing to ensure secure and reliable authentication.
