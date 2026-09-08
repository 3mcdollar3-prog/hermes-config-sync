# Hermes Manual Backup Workflow (Ad-hoc)

If automated `hermes-sync` tools are unavailable or need customization, follow this procedure to manually backup state to GitHub:

1.  **Stage Files**:
    ```bash
    mkdir -p ~/hermes_backup_$(date +%Y%m%d)
    cp ~/.hermes/config.yaml ~/hermes_backup_$(date +%Y%m%d)/
    cp -r ~/.hermes/configs/ ~/.hermes/skills/ ~/.hermes/cron/ ~/.hermes/memories/ ~/.hermes/sessions/ ~/hermes_backup_$(date +%Y%m%d)/
    ```

2.  **Repo Initialization**:
    ```bash
    cd ~/hermes_backup_$(date +%Y%m%d)
    git init
    git branch -m main
    git config user.email "hermes-backup@example.com"
    git config user.name "Hermes Backup Agent"
    git add .
    git commit -m "Backup: $(date)"
    ```

3.  **Push via gh**:
    ```bash
    gh repo create hermes-backup-$(date +%Y%m%d) --private --source=. --remote=origin --push
    ```
