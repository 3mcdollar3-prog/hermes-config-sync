import os
import subprocess
import sys

# The scripts are located in the skill's directory
SKILL_DIR = os.path.expanduser("~/.hermes/skills/hermes-sync")
SYNC_SCRIPT = os.path.join(SKILL_DIR, "scripts/sync_to_repo.py")
DEPLOY_SCRIPT = os.path.join(SKILL_DIR, "scripts/deploy_sync.py")

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def sync():
    if not os.path.exists(SYNC_SCRIPT):
        return f"Error: Sync script not found at {SYNC_SCRIPT}"
    return run_command(["python3", SYNC_SCRIPT])

def deploy(repo_path):
    if not os.path.exists(DEPLOY_SCRIPT):
        return f"Error: Deploy script not found at {DEPLOY_SCRIPT}"
    if not os.path.exists(repo_path):
        return f"Error: Repo path {repo_path} does not exist."
    return run_command(["python3", DEPLOY_SCRIPT, repo_path])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: hermes-sync.py [sync|deploy <repo_path>]")
        sys.exit(1)
    
    action = sys.argv[1]
    if action == "sync":
        print(sync())
    elif action == "deploy" and len(sys.argv) == 3:
        print(deploy(sys.argv[2]))
    else:
        print("Invalid usage.")
        sys.exit(1)
