---
name: shopify-auth-bypass
description: Workaround for Shopify CLI authentication in headless agent environments.
---
# Shopify CLI Auth Bypass for Background Deployment

This skill provides a workaround for the Shopify CLI's requirement for interactive authentication in headless environments.

## The Problem
Shopify CLI `hydrogen link` and `deploy` commands require a browser-based OAuth flow which fails in non-interactive/background terminal sessions because it cannot open the browser or wait for the user to complete the login on the host machine.

## The Workaround (Manual Sync)
Since we cannot bridge the local browser auth to a background headless shell, we must authenticate in a persistent, interactive session once, and then share the configuration.

### Steps to Solve
1. **Interactive Authentication:**
   Run the following in an interactive terminal (your main CLI window):
   ```bash
   # Run this once on your host machine to get the token/state
   npm install -g @shopify/cli
   shopify login --store=<YOUR_STORE_DOMAIN>
   ```

2. **Sync Configuration:**
   Once logged in, the CLI stores credentials in `~/.config/shopify/`.
   Copy these credentials into the environment that the Hermes Agent uses, or use the project-local link:
   ```bash
   cd <project_dir>
   npx shopify hydrogen link --store=<YOUR_STORE_DOMAIN>
   ```

3. **Background Deployment (The Agent Part):**
   Once the project directory contains the authenticated `shopify.app.toml` and `.env` files, the Hermes Agent can perform non-interactive deployments:
   ```bash
   cd <project_dir>
   npx shopify hydrogen deploy --env=Preview
   ```

## Pitfalls
- **No Browser Sync:** The agent cannot "see" your browser, so it will always fail at `shopify login`.
- **Cached Auth:** If auth files are deleted, the agent will never be able to deploy.
- **Organization Mismatch:** Ensure you have logged in to the correct Shopify organization account.
