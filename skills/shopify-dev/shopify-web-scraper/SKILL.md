---
name: shopify-web-scraper
description: "Scrapers and bulk import tools for Shopify stores, following Shopify CSV standards."
---

# Shopify Web Scraper

This skill provides local-only scraping and import utilities for Shopify stores. It avoids external paid APIs by using local Python environments.

## Bulk Import Script (`scripts/bulk_import.py`)
Parses local CSV files and image folders to create products via Shopify Admin API.

### **Functionality**: 
1. Creates a new Shopify store using `shopify app init`.
2. Imports products from a specified CSV and associates images.

### **CSV Format**
Ensure your CSV follows the official [Shopify Product CSV format](https://help.shopify.com/en/manual/products/import-export/using-csv).
Required headers: `Handle`, `Title`, `Body (HTML)`, `Vendor`, `Type`, `Tags`, `Option1 Name`, `Option1 Value`, `Variant Price`, `Variant SKU`, `Image Src`.

## MCP Server (Local)
Defined as a stdio server in `~/.hermes/config.yaml`:
```yaml
mcp_servers:
  shopify-scraper:
    command: "python3"
    args: ["/home/mcdollar3/.hermes/scripts/shopify_scraper_mcp.py"]
```

## Setup Instructions
1. Save your product CSVs in `/home/mcdollar3/shopify_imports/`.
2. Save product images in corresponding subfolders.
3. Run import via terminal:
   `python3 /home/mcdollar3/.hermes/scripts/bulk_import.py --csv /path/to/file.csv --images /path/to/img_dir/`

## Troubleshooting & Workflow
- Use `/home/mcdollar3/shopify_imports/products.csv` as the reference standard.
- The `bulk_import.py` now expects images to be pulled directly from the URLs provided in the CSV column `Image Src`.
