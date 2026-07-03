#!/bin/bash

# Configuration: List of models in order of priority
MODELS=("gemini-3.1-flash-lite" "gemini-2.5-flash" "gemini-3.5-flash" "gemini-3.1-pro-preview" "gemini-3.1-flash" "gemini-2.5-pro")

# Get the current model
CURRENT=$(hermes config | grep -o "'default': '[^']*'" | cut -d"'" -f4)

# Find the index of the current model
IDX=-1
for i in "${!MODELS[@]}"; do
   if [[ "${MODELS[$i]}" == "$CURRENT" ]]; then
       IDX=$i
       break
   fi
done

# Calculate the next index
NEXT_IDX=$(( (IDX + 1) % ${#MODELS[@]} ))
NEXT_MODEL=${MODELS[$NEXT_IDX]}

echo "Switching from $CURRENT to $NEXT_MODEL..."

# Apply the switch
hermes config set model.default $NEXT_MODEL
