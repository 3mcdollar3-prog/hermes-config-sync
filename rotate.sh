#!/bin/bash

# Source the Hermes environment variables
if [ -f "$HOME/.hermes/.env" ]; then
  source "$HOME/.hermes/.env"
fi

# Run the Python model rotation script
python ~/.hermes/scripts/rotate_model.py
