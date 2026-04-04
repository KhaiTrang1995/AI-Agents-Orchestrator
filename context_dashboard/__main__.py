"""Entry point for python -m context_dashboard."""

from context_dashboard.app import app

app.run(host="0.0.0.0", port=5003, debug=False)
