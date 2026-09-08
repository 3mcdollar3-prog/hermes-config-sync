#!/bin/bash
APP_NAME=${1:-"shop-factory-$(date +%s)"}
ORG_ID="228710689"

echo "Creating Shopify App: $APP_NAME"
shopify app init \
  --name "$APP_NAME" \
  --organization-id "$ORG_ID" \
  --template none \
  --package-manager npm
