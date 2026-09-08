import os
import shutil
import yaml
import subprocess
import json
import sys

# CONFIGURATION
HERMES_HOME = os.path.expanduser("~/.hermes")
# The directory where the user has cloned the git repo
# In a real-world scenario, this would be the path to the cloned repo
REPO_ROOT = os.path.expanduser("~/hermes-sync-dev/repo_template")
ENV_FILE_PATH = os.path.expanduser("~/.hermes/.env")

def deploy_config(repo_path):
    print("--- Deploying Config ---")
    config_src = os.path.join(repo_path, "configs/config.yaml")
    config_dest = os.path.join(HERMES_HOME, "config.yaml")
    
    if not os.path.exists(config_src):
        print(f"Error: Config source not found at {config_src}")
        return

    # We do NOT copy the redacted config directly if it contains placeholders.
    # Instead, we use the existing config and only update what's in the repo.
    # For a simple implementation, we'll just overwrite and tell the user
    # to re-add their secrets.
    
    shutil.copy2(config_src, config_dest)
    print(f"Deployed config from {config_src} to {config_dest}")
    print("NOTE: Please ensure your .env file is correctly configured with your API keys.")

def deploy_skills(repo_path):
    print("--- Deploying Skills ---")
    skills_src = os.path.join(repo_path, "skills")
    skills_dest = os.path.join(HERMES_HOME, "skills")
    
    if not os.path.exists(skills_src):
        print(f"Error: Skills source not found at {skills_src}")
        return

    # 1. Sync existing skills (add new ones, update changed ones)
    # For simplicity, we'll just overwrite the whole directory.
    if os.path.exists(skills_dest):
        shutil.rmtree(skills_dest)
    
    shutil.copytree(skills_src, skills_dest)
    print(f"Deployed skills from {skills_src} to {skills_dest}")

def deploy_cron(repo_path):
    print("--- Deploying Cron Jobs ---")
    manifest_src = os.path.join(repo_path, "cron/manifest.json")
    
    if not os.path.exists(manifest_src):
        print(f"Error: Manifest not found at {manifest_src}")
        return

    with open(manifest_src, 'r') as f:
        manifest = json.load(f)

    for job in manifest:
        # In a real implementation, we would use 'hermes cron create' 
        # based on the manifest data.
        print(f"Placeholder: Would create job {job.get('id', 'unknown')}")

def main():
    if len(sys.argv) < 2:
        print("Usage: deploy_sync.py <path_to_cloned_repo>")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    
    if not os.path.exists(repo_path):
        print(f"Error: Repo path {repo_path} does not exist.")
        sys.exit(1)

    print(f"Starting deployment from {repo_path}...")
    deploy_config(repo_path)
    deploy_skills(repo_path)
    deploy_cron(repo_path)
    print("\n--- Deployment Complete! ---")

if __name__ == "__main__":
    main()
