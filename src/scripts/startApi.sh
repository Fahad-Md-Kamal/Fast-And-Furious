#!/bin/sh
# start.sh

# Ensure script fails if any command fails
set -e

# Start the Uvicorn server with specific options
poetry run uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000
