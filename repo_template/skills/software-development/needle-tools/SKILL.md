---
name: needle-tools
description: "Use Needle 2 for local high-speed structured extraction."
version: 1.0.0
author: Hermes Agent
---

# Needle Tools

This skill wraps the Needle 2 engine for local, high-speed structured extraction and tool-calling. It allows Hermes to perform parsing tasks locally without remote LLM calls.

## Tools

### `needle_extract`
Performs structured extraction from raw text.

- **Parameters**:
  - `text`: (str) Raw text to extract from.
  - `schema_name`: (str) Name for the model.
  - `schema_fields`: (dict) Mapping of field names to type strings (e.g., `{'total': 'float'}`).

## Implementation

The skill invokes the `needle_tool` bridge tool registered in Hermes. Ensure `cactus-needle` is installed in your Hermes venv:
`pip install cactus-needle`

## Example Usage

"Extract invoice details from this text: [invoice text]. Use total as float and vendor as string."
