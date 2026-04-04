"""Allow ``python -m mcp_server`` to start the server."""

from mcp_server.server import *  # noqa: F401,F403

# Re-run the server's __main__ block
if __name__ == "__main__":
    import runpy

    runpy.run_module("mcp_server.server", run_name="__main__", alter_sys=True)
