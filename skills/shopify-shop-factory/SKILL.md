---
name: shopify-shop-factory
description: "Manages the creation and basic setup of Shopify stores and apps."
---

# Shopify Shop Factory

This skill provides functions to automate the creation of Shopify stores and the initial setup of associated apps.

## Functions

### create_shop

Creates a new Shopify development store and a basic app using the Shopify CLI.

**Parameters**:

*   `org_id` (str): Your Shopify Partner Organization ID.
*   `app_name` (str, optional): Name for the new Shopify app. Defaults to a generated name.
*   `template` (str, optional): Shopify app template to use. Defaults to "none".
*   `package_manager` (str, optional): Package manager to use. Defaults to "npm".

**Returns**:

*   A dictionary containing information about the created app and store (e.g., app name, store URL, store admin URL).

**Pitfalls**:

*   Shopify CLI authentication: Ensure the CLI is logged in to your partner account.
*   Interactive prompts: `shopify app init` can be interactive. Flags should minimize this, but explicit handling might be needed.
*   Rate limits: While less likely for initial creation, be mindful of API rate limits for subsequent operations.

## Unified Hydrogen Shop Factory Orchestration
- Use the unified orchestration script (`shop_factory.py`) to automate Shopify app scaffolding, CSV inventory ingestion, Hydrogen mock data injection, and environment configuration in a single execution.
- **Inventory Ingestion**: Parses standardized CSV catalogs (`shopify_products.csv`) and seeds Hydrogen mock stores or Admin APIs.
- **Non-Interactive Bypasses**: When running CLI scaffolding tools like `create-hydrogen`, handle non-interactive terminal restrictions gracefully by providing default fallbacks or structure templates.

## Model Quotas & Retries
To avoid hitting maximum retry limits (like HTTP 429) on a single Gemini model, lower the retry count in `~/.hermes/config.yaml`:
```yaml
agent:
  api_max_retries: 2
```
This forces Hermes to quickly trigger the `credential_pool_strategies` rotation instead of repeatedly retrying an exhausted model.

## Non-Interactive Troubleshooting
When running Shopify CLI commands in a non-interactive (automated) shell:
- **Authentication**: `shopify hydrogen link` and `deploy` often fail due to interactive prompts for shop selection. **Always** instruct the user to run these commands manually in their terminal to authorize the session.
- **Git Requirement**: Deployments to Oxygen require a Git repository in the project folder. Run `git init && git add . && git commit -m "Initial commit"` before deploying.
- **Forced Updates**: For automated environments, use the `--force` flag for deployment if uncommitted changes exist, though a clean commit is preferred for stability.
- **Timeouts**: If a command hangs on a prompt, it will hit a timeout. Do not re-run in background mode; instead, surface the exact prompt error to the user for manual intervention.


### Authentication & Org IDs
- **Organization IDs**: Always run `shopify organization list` to find the correct numerical `ID`. Do NOT use `shpss_` API tokens.
- **Non-Interactive Environments**: CLI commands like `shopify app init` can time out in background-driven sessions. If a command hits a timeout, verify the directory creation (`ls -d <app_name>/`) before retrying.
- **Linking Configuration**: If `shopify app config link` fails, ensure you have a `client_id` from the Partner Dashboard.
- **Deploying Extensions**: Non-interactive deployments require `shopify app deploy --allow-updates`.

### Browser Automation as a Crawler
- If web-crawling tools (e.g., Firecrawl) are restricted or failing, use the `mcp__chrome_devtools` toolset to navigate and extract content directly from the page.

### Reference
- See `references/non-interactive-troubleshooting.md` for handling CLI timeouts and common errors.


## Example Usage

```bash
# Check organization ID first
shopify organization list

# Create the app
shopify app init --name <name> --organization-id <id> --template none --package-manager npm
```
