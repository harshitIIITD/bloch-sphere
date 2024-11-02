#!/bin/bash

# Check if the virtual environment exists, activate it if it does.
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "Virtual environment '.venv' not found. Please create it first."
    exit 1
fi

# Set a default port if $PORT is not set.
PORT=${PORT:-5000}

# Run the Flask application in debug mode.
python -m flask --app app run -p "$PORT" --debug
