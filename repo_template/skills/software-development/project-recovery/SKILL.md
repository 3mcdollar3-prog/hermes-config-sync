---
name: project-recovery
description: "Workflow for recovering projects after unexpected crashes, interruptions, or lost local state."
version: 1.0.0
---

# Project Recovery Workflow

Use this skill when a project was interrupted by a crash or unexpected shutdown.

## Recovery Checklist

1. **Locate the project:**
   - Use `ls -d */` or `search_files(target='files')` to identify the project root.
2. **Verify environment integrity:**
   - Check for `package.json` (Node), `requirements.txt` (Python), or equivalent dependency files.
   - Run `npm install` (Node) or `pip install` (Python) to restore missing modules.
3. **Diagnose state:**
   - Look for lockfiles (e.g., `package-lock.json`, `poetry.lock`).
   - If a build or server fails with `ENOENT` or `module not found` after a crash, remove the lockfile and `node_modules` (or venv) directory, then reinstall dependencies.
4. **Restart processes:**
   - Identify the correct start command (e.g., `npm run dev`) from `README.md` or past sessions.
   - Run the process using `terminal(background=true)` and monitor logs.
5. **Verify output:**
   - Once the server indicates readiness, access the local preview URL (e.g., `http://localhost:3000`).

## Pitfalls
- **Corrupted Lockfiles:** Crash-interrupted package managers often produce broken lockfiles. Always delete and reinstall if `npm run dev` fails with module-related errors.
- **Ghost Processes:** Check for orphaned processes (`ps aux`) if the new server fails to bind to the port.
