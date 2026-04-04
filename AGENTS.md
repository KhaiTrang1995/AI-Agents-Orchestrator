# AGENTS.md — Instructions for AI Coding Agents

This file is read by Codex, Gemini CLI, and other agentic coding tools. Claude Code reads `.claude/CLAUDE.md` which imports this file.

## Project Overview
AI Coding Tools Orchestrator: two self-contained systems coordinating AI coding assistants (Claude, Codex, Gemini, Copilot, Ollama, llama.cpp).

## Build & Test
```bash
pip install -r requirements.txt
python -m pytest tests/ --override-ini="addopts=" -q --timeout=30 -m "not integration and not slow"
```

## Code Style
- Python 3.8+, type hints required
- Black formatting, 120-char max line length
- isort for import ordering
- flake8 for linting

## Architecture Boundaries
- `orchestrator/` and `agentic_team/` are fully independent — zero shared imports
- Each has its own adapters/, config/, ui/, CLI
- `mcp_server/` is optional and depends on both

## Testing
- All tests in `tests/` directory
- Use `@pytest.mark.integration` for tests requiring CLI tools (claude, codex, gemini)
- Use `@pytest.mark.slow` for long-running tests
- CI excludes integration and slow tests

## File Patterns
- Adapters: `*/adapters/<name>_adapter.py` extending `BaseAdapter`
- Config: `*/config/agents.yaml` (YAML, not JSON)
- Tests: `tests/test_<module>.py`
