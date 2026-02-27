#!/bin/bash
# Startup script for standalone Agentic Team UI

set -e

echo "Starting Agentic Team UI (standalone)"

if [ ! -d "ui/venv" ]; then
  cd ui
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  pip install httpx
  cd ..
else
  cd ui
  source venv/bin/activate
  pip install -r requirements.txt >/dev/null
  pip install httpx >/dev/null
  cd ..
fi

source ui/venv/bin/activate
python ui/agentic_app.py
