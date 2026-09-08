---
name: shopify-create-shop
description: "Scaffold a new Shopify app and development store automatically."
---

# Shopify Create Shop

This skill automates the initialization of a Shopify app using the Shopify CLI.

## Usage
`hermes skills run shopify-create-shop --app-name <name>`

## Logic
1. Runs `shopify app init` with non-interactive flags.
2. Uses the Partner Organization ID (`228710689`).
3. Sets up a clean development store environment.
4. **Hydrogen Storefront Integration**: Scaffolds a high-performance Hydrogen storefront (`npm create @shopify/hydrogen@latest`), binding Storefront API tokens and store domains to environment variables (`PUBLIC_STOREFRONT_API_TOKEN`, `PUBLIC_STORE_DOMAIN`).
5. **Creates a Shopify store and app via the Shopify Admin API**, and imports products from a provided CSV and image directory.

## Pitfalls
- **Organization ID**: Use `shopify organization list` to find the correct `ID`, not a `shpss_` prefix (which is an API token).
- **Non-Interactive Errors**: In non-interactive terminals, some CLI commands require `--force` or specific file flags like `--file-name` to prevent prompting. If a command fails, check `--help` for non-interactive equivalents.
- **Dependency Timeouts**: Large initializations (like `shopify app init`) can time out in constrained environments. If they do, verify if the directory was created; if so, continue with extension generation using existing project files.
- **Linking Configuration**: `shopify app config link` requires a valid, pre-existing Client ID from the Shopify Partner Dashboard. It cannot create the app shell itself.

## Script
```bash
#!/bin/bash
# Path: scripts/init-shop.sh
APP_NAME=${1:-"shop-factory-$(date +%s)"}
ORG_ID="228710689"

shopify app init \
  --name "$APP_NAME" \
  --organization-id "$ORG_ID" \
  --template none \
  --package-manager npm
```
