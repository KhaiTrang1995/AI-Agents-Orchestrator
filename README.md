# AI Coding Tools Orchestrator and Agentic Team Runtime

![Claude](https://img.shields.io/badge/Claude-Anthropic-D97706?logo=anthropic&logoColor=white)
![OpenAI Codex](https://img.shields.io/badge/Codex-OpenAI-412991?logo=openai&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-Google-4285F4?logo=google&logoColor=white)
![GitHub Copilot](https://img.shields.io/badge/Copilot-GitHub-000000?logo=githubcopilot&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-000000?logo=ollama&logoColor=white)
![llama.cpp](https://img.shields.io/badge/llama.cpp-GGUF-8B5CF6?logo=meta&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Model Context Protocol](https://img.shields.io/badge/MCP-Model_Context_Protocol-4A90D9?logo=modelcontextprotocol&logoColor=white)
![FastMCP](https://img.shields.io/badge/FastMCP-3.x-black?logo=modelcontextprotocol&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.x-E92063?logo=pydantic&logoColor=white)
![Click](https://img.shields.io/badge/Click-8.x-000000?logo=python&logoColor=white)
![Rich](https://img.shields.io/badge/Rich-13.x-009485?logo=python&logoColor=white)
![HTTPX](https://img.shields.io/badge/HTTPX-0.27-3776AB?logo=python&logoColor=white)
![Tenacity](https://img.shields.io/badge/Tenacity-Retry-3776AB?logo=python&logoColor=white)
![Structlog](https://img.shields.io/badge/Structlog-Logging-3776AB?logo=python&logoColor=white)
![PyYAML](https://img.shields.io/badge/PyYAML-6.x-3776AB?logo=yaml&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vue.js&logoColor=white)
![Nuxt](https://img.shields.io/badge/Nuxt-3.x-00C58E?logo=nuxt.js&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-5.x-646CFF?logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind-3.x-06B6D4?logo=tailwindcss&logoColor=white)
![Pinia](https://img.shields.io/badge/Pinia-State-FFD859?logo=vue.js&logoColor=white)
![Monaco](https://img.shields.io/badge/Monaco_Editor-VS_Code-007ACC?logo=visualstudiocode&logoColor=white)
![Socket.IO](https://img.shields.io/badge/Socket.IO-4.x-010101?logo=socket.io&logoColor=white)
![Axios](https://img.shields.io/badge/Axios-HTTP-5A29E4?logo=axios&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-E6522C?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800?logo=grafana&logoColor=white)
![Bandit](https://img.shields.io/badge/Bandit-Security_Scan-FFD43B?logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-314_Tests-0A9EDC?logo=pytest&logoColor=white)
![MyPy](https://img.shields.io/badge/MyPy-Type_Checked-3776AB?logo=python&logoColor=white)
![Black](https://img.shields.io/badge/Code_Style-Black-000000?logo=python&logoColor=white)
![Flake8](https://img.shields.io/badge/Linter-Flake8-4B8BBE?logo=python&logoColor=white)
![isort](https://img.shields.io/badge/isort-Imports-EF8336?logo=python&logoColor=white)
![Pre-commit](https://img.shields.io/badge/Pre--commit-Hooks-FAB040?logo=precommit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5?logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-IaC-844FBA?logo=terraform&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-Reverse_Proxy-009639?logo=nginx&logoColor=white)
![HAProxy](https://img.shields.io/badge/HAProxy-Load_Balancer-009639?logo=haproxy&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?logo=githubactions&logoColor=white)
![GitLab CI](https://img.shields.io/badge/GitLab_CI-Pipeline-FC6D26?logo=gitlab&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-Pipeline-D24939?logo=jenkins&logoColor=white)
![Microsoft Azure](https://img.shields.io/badge/Azure-Cloud-0078D4?logo=microsoftazure&logoColor=white)
![systemd](https://img.shields.io/badge/systemd-Services-4EAA25?logo=linux&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-green?logo=opensourceinitiative&logoColor=white)
![Mermaid Diagrams](https://img.shields.io/badge/Mermaid_Diagrams-132-FF3670?logo=mermaid&logoColor=white)

<div align="center">

**Two self-contained systems -- an AI Orchestrator and an Agentic Team runtime -- that coordinate cloud and local AI coding assistants (Claude, Codex, Gemini, Copilot, Ollama, llama.cpp) to collaborate on software development tasks.**

[Overview](#overview) | [Architecture](#architecture) | [System Comparison](#system-comparison) | [Features](#feature-highlights) | [Quick Start](#quick-start) | [Project Structure](#project-structure) | [Configuration](#configuration) | [Deployment](#deployment) | [Testing](#testing) | [MCP Server](#mcp-server-optional----model-context-protocol)

</div>

---

## Overview

AI Coding Tools ships two completely independent systems in a single repository. The **Orchestrator** runs step-based workflows where AI agents execute tasks in sequence (implement, review, refine). The **Agentic Team** runs a free-communication runtime where role-based agents (Project Manager, Architect, Developer, QA, DevOps) discuss a task in turns until the team lead declares the work complete. Each system carries its own adapters, configuration, UI, and CLI -- they share zero code and zero imports.

## Architecture

### High-Level Overview

```mermaid
graph TD
    subgraph Repository["AI Coding Tools Repository"]
        direction TB

        subgraph Orchestrator["orchestrator/"]
            O_CLI["CLI Shell"]
            O_UI["Web UI<br/>Nuxt 3 + Flask + Socket.IO"]
            O_CORE["Core Engine<br/>Workflow Manager<br/>Task Manager"]
            O_ADAPT["Adapters<br/>Claude | Codex | Gemini<br/>Copilot | Ollama | llama.cpp"]
            O_RESIL["Resilience<br/>Retry | Fallback | Offline"]
            O_OBS["Observability<br/>Prometheus | Logging | Health"]
            O_SEC["Security Module<br/>Validation | Rate Limiting | Audit"]
            O_INFRA["Infra<br/>Cache | Async Executor | Config Manager"]
            O_CONF["orchestrator/config/agents.yaml"]
        end

        subgraph AgenticTeam["agentic_team/"]
            A_CLI["CLI REPL"]
            A_UI["Web UI<br/>Nuxt 3 + Flask + Socket.IO"]
            A_ENGINE["Engine<br/>Free Communication<br/>Lead-Gated Output"]
            A_ADAPT["Adapters<br/>Claude | Codex | Gemini<br/>Copilot | Ollama | llama.cpp"]
            A_FALLBACK["Fallback + Offline"]
            A_CONF["orchestrator/config/agents.yaml"]
        end
    end

    O_CLI --> O_CORE
    O_UI --> O_CORE
    O_CORE --> O_ADAPT
    O_CORE --> O_RESIL
    O_CORE --> O_OBS
    O_CORE --> O_SEC
    O_CORE --> O_INFRA
    O_ADAPT --> ExtCloud["Cloud CLIs<br/>claude | codex | gemini | copilot"]
    O_ADAPT --> ExtLocal["Local Backends<br/>Ollama | llama.cpp"]

    A_CLI --> A_ENGINE
    A_UI --> A_ENGINE
    A_ENGINE --> A_ADAPT
    A_ENGINE --> A_FALLBACK
    A_ADAPT --> ExtCloud
    A_ADAPT --> ExtLocal

    style Orchestrator fill:#1a1a2e,stroke:#16213e,color:#e0e0e0
    style AgenticTeam fill:#1a2e1a,stroke:#162e16,color:#e0e0e0
```

### Orchestrator Workflow Execution

The Orchestrator processes tasks through a configurable pipeline of AI agents. Each step in a workflow maps to a specific agent and role.

```mermaid
sequenceDiagram
    participant User
    participant CLI as CLI / Web UI
    participant Engine as Core Engine
    participant WF as Workflow Manager
    participant Codex as Codex Adapter
    participant Gemini as Gemini Adapter
    participant Claude as Claude Adapter
    participant FB as Fallback Manager

    User->>CLI: Submit task
    CLI->>Engine: execute(task, workflow="default")
    Engine->>WF: load workflow steps

    WF->>Codex: Step 1 -- implement
    alt Codex unavailable
        Codex-->>FB: error
        FB->>FB: route to local-code
    end
    Codex-->>WF: implementation

    WF->>Gemini: Step 2 -- review
    Gemini-->>WF: review feedback

    WF->>Claude: Step 3 -- refine
    Claude-->>WF: refined code

    WF-->>Engine: final result
    Engine-->>CLI: display output
    CLI-->>User: code + report
```

### Agentic Team Communication Flow

The Agentic Team uses free role-to-role communication. Agents speak in turns, address each other by role, and the team lead decides when the task is complete.

```mermaid
sequenceDiagram
    participant User
    participant PM as Project Manager (Lead)
    participant Arch as Software Architect
    participant Dev as Software Developer
    participant QA as QA Engineer
    participant DevOps as DevOps Engineer

    User->>PM: "Build a REST API with auth"
    PM->>Arch: Define architecture and constraints
    Arch->>Dev: Provide interface specs
    Dev->>Dev: Implement code
    Dev->>QA: Request quality review
    QA->>Dev: Report edge cases
    Dev->>Dev: Fix issues
    Dev->>DevOps: Request deployment review
    DevOps->>PM: Confirm operational readiness
    PM->>User: Final consolidated response
```

### Adapter Resolution Flow

Both systems resolve which AI backend to use at runtime. The adapter layer abstracts cloud CLIs and local model servers behind a common interface.

```mermaid
flowchart TD
    REQ[Incoming Task Step] --> CHECK{Agent Enabled?}
    CHECK -->|Yes| HEALTH{Health Check}
    CHECK -->|No| SKIP[Skip Agent]

    HEALTH -->|Healthy| EXEC[Execute via Adapter]
    HEALTH -->|Unhealthy| FB{Fallback Configured?}

    FB -->|Yes| LOCAL[Route to Local Adapter<br/>Ollama / llama.cpp]
    FB -->|No| ERR[Raise AgentUnavailableError]

    EXEC --> PARSE[Parse CLI Output]
    LOCAL --> PARSE
    PARSE --> RESULT[Return AgentResponse]

    style EXEC fill:#2b6cb0,stroke:#2c5282,color:#fff
    style LOCAL fill:#276749,stroke:#22543d,color:#fff
    style ERR fill:#9b2c2c,stroke:#742a2a,color:#fff
```

### Technology Stack Overview

```mermaid
graph LR
    subgraph Backend
        PY[Python 3.8+]
        FL[Flask 3.x]
        SIO[Socket.IO 4.x]
        PD[Pydantic 2.x]
        CL[Click 8.x]
    end

    subgraph Frontend
        VUE[Vue 3]
        NUXT[Nuxt 3]
        TW[Tailwind CSS 3.x]
        MON[Monaco Editor]
        PIN[Pinia]
    end

    subgraph Observability
        PROM[Prometheus]
        GRAF[Grafana]
        SL[structlog]
    end

    subgraph Infrastructure
        DOCK[Docker]
        K8S[Kubernetes]
        TF[Terraform]
    end

    PY --> FL --> SIO
    PY --> PD
    PY --> CL
    VUE --> NUXT --> TW
    VUE --> MON
    VUE --> PIN
    PROM --> GRAF
    DOCK --> K8S

    style Backend fill:#1a1a2e,stroke:#16213e,color:#e0e0e0
    style Frontend fill:#1a2e1a,stroke:#162e16,color:#e0e0e0
    style Observability fill:#2e1a1a,stroke:#2e1616,color:#e0e0e0
    style Infrastructure fill:#1a1a2e,stroke:#16213e,color:#e0e0e0
```

## System Comparison

The two systems serve different collaboration models. Choose based on your use case.

| Dimension | Orchestrator (`orchestrator/`) | Agentic Team (`agentic_team/`) |
|---|---|---|
| **Collaboration model** | Step-based pipeline (sequential) | Free role-to-role communication (turns) |
| **Agent identity** | Tool names (codex, gemini, claude) | Roles (PM, Architect, Developer, QA, DevOps) |
| **Control flow** | Workflow YAML defines fixed step order | Team lead (PM) gates completion dynamically |
| **When to use** | Repeatable pipelines: implement, review, refine | Open-ended tasks needing discussion and consensus |
| **CLI entry point** | `ai-orchestrator shell` | `ai-orchestrator agentic-shell` |
| **Web UI port** | `:5001` | `:5002` |
| **Config file** | `orchestrator/config/agents.yaml` | `agentic_team/config/agents.yaml` |
| **Built-in workflows** | 7 (default, quick, thorough, review-only, document, offline-default, hybrid) | N/A (turn-based, no fixed pipeline) |
| **Fallback strategy** | Per-step cloud-to-local routing | Independent fallback manager |
| **Observability** | Prometheus metrics, structured logging, health probes | Health and readiness probes |
| **Security module** | Input validation, rate limiting, audit logging | N/A (inherits from adapter layer) |
| **Shared code** | None | None |

## Feature Highlights

### Orchestrator (`orchestrator/`)

| Category | Features |
|---|---|
| **Workflows** | 7 built-in workflows (default, quick, thorough, review-only, document, offline-default, hybrid); define custom ones in YAML |
| **Agents** | Claude, Codex, Gemini, Copilot (cloud); Ollama, llama.cpp (local) |
| **CLI** | Interactive REPL shell, one-shot commands, context-aware follow-ups, readline support |
| **Web UI** | Nuxt 3 + Vue 3 frontend, Flask + Socket.IO backend, Monaco code editor, Pinia state management |
| **Resilience** | Retry with exponential backoff, circuit breakers, cloud-to-local fallback, offline detection |
| **Observability** | Prometheus metrics, structured logging via structlog, health and readiness probes |
| **Security** | Input validation, rate limiting, secret management, audit logging |
| **Infra** | Async executor, response caching, connection pooling, config manager |

### Agentic Team (`agentic_team/`)

| Category | Features |
|---|---|
| **Runtime** | Free role-to-role communication, configurable turn limits, lead-gated final responses |
| **Roles** | Project Manager, Software Architect, Software Developer, QA Engineer, DevOps Engineer |
| **CLI** | Dedicated REPL (`agentic-shell`) with `--max-turns` and `--offline` flags |
| **Web UI** | Dedicated Nuxt 3 + Flask UI with Config Studio, real-time turn streaming, team communication view |
| **Fallback** | Independent fallback manager and offline detector |
| **Configuration** | Separate `agents.yaml` with `agentic_team.roles` section for role-to-agent mapping |

## Quick Start

### Prerequisites

- **Operating System**: Linux, macOS, or Windows (WSL recommended)
- **Python**: 3.8 or higher
- **Node.js**: 20+ (for Web UI)
- **Memory**: Minimum 4GB RAM
- **Disk Space**: 1GB for installation + workspace
- **Network**: Required for AI CLI tools and updates
- **Claude Code**: Installed, setup, and signed in on your machine (Required for any workflows using Claude Code - if you run `claude` in terminal and it works, you're good)
- **OpenAI Codex**: Installed and authenticated (if using Codex agent, try running `codex` and see if it responds)
- **Google Gemini CLI**: Installed and authenticated (if using Gemini agent, try `gemini --version` to verify)
- **GitHub Copilot CLI**: Installed and authenticated (if using Copilot agent, try `copilot --version` to verify)
- **Llama.cpp or Ollama**: If using local LLM agents, ensure they are installed and configured properly (try running `ollama list` or `llamacpp --help` to verify)
- **Optional**: Docker and Docker Compose for containerized setup

### Install

```bash
git clone https://github.com/hoangsonww/AI-Agents-Orchestrator.git
cd AI-Agents-Orchestrator

python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
chmod +x ai-orchestrator
```

### Run the Orchestrator

```bash
# Interactive shell
./ai-orchestrator shell

# One-shot task
./ai-orchestrator run "Create a Python REST API" --workflow default

# Start the Web UI
make run-ui
# Then open http://localhost:5001
```

### Run the Agentic Team

```bash
# Interactive REPL
./ai-orchestrator agentic-shell

# With options
./ai-orchestrator agentic-shell --max-turns 16 --offline

# Start the Web UI
make run-agentic-ui
# Then open http://localhost:5002
```

### Verify Installation

```bash
./ai-orchestrator --help        # Show all commands
./ai-orchestrator agents        # List available agents
./ai-orchestrator workflows     # List available workflows
./ai-orchestrator validate      # Validate configuration
```

## Project Structure

```
AI-Coding-Tools/
|
|-- mcp_server/                      # MCP server (FastMCP 3.x)
|   |-- server.py                    # 10 tools + 2 resources
|
|-- orchestrator/                    # Self-contained orchestrator system
|   |-- __init__.py
|   |-- adapters/                    # AI agent adapters
|   |   |-- base.py                  #   Abstract base adapter
|   |   |-- claude_adapter.py        #   Claude Code CLI
|   |   |-- codex_adapter.py         #   OpenAI Codex CLI
|   |   |-- gemini_adapter.py        #   Google Gemini CLI
|   |   |-- copilot_adapter.py       #   GitHub Copilot CLI
|   |   |-- ollama_adapter.py        #   Ollama local models
|   |   |-- llama_cpp_adapter.py     #   llama.cpp / OpenAI-compatible
|   |   +-- cli_communicator.py      #   Robust CLI subprocess handling
|   |-- core/                        # Core orchestration logic
|   |   |-- engine.py                #   Main orchestration engine
|   |   |-- workflow.py              #   Workflow definitions and runner
|   |   |-- task_manager.py          #   Task lifecycle management
|   |   +-- exceptions.py            #   Custom exception hierarchy
|   |-- resilience/                  # Fault tolerance
|   |   |-- retry.py                 #   Retry with exponential backoff
|   |   |-- fallback.py              #   Cloud-to-local fallback routing
|   |   +-- offline.py               #   Offline detection
|   |-- observability/               # Monitoring and logging
|   |   |-- metrics.py               #   Prometheus metrics
|   |   |-- logging_config.py        #   Structured logging setup
|   |   +-- health.py                #   Health and readiness probes
|   |-- security_module/             # Security layer
|   |   +-- security.py              #   Validation, rate limiting, audit
|   |-- infra/                       # Infrastructure utilities
|   |   |-- cache.py                 #   Response caching
|   |   |-- async_executor.py        #   Async task execution
|   |   +-- config_manager.py        #   Configuration loading
|   |-- cli/                         # CLI interface
|   |   +-- shell.py                 #   Interactive REPL shell
|   |-- config/
|   |   +-- agents.yaml              #   Agents, workflows, settings
|   |-- ui/                          # Web UI
|   |   |-- app.py                   #   Flask + Socket.IO backend
|   |   |-- frontend/                #   Nuxt 3 + Vue 3 + Tailwind
|   |   |-- static/
|   |   +-- templates/
|   +-- README.md                    #   Orchestrator-specific docs
|
|-- agentic_team/                    # Self-contained agentic team system
|   |-- __init__.py
|   |-- engine.py                    # Role-based communication engine
|   |-- shell.py                     # Agentic team REPL
|   |-- decision_parser.py           # Turn decision parsing
|   |-- config_utils.py              # Config loading utilities
|   |-- constants.py                 # Shared constants
|   |-- fallback.py                  # Independent fallback manager
|   |-- offline.py                   # Independent offline detector
|   |-- adapters/                    # Own copy of AI agent adapters
|   |   |-- base.py
|   |   |-- claude_adapter.py
|   |   |-- codex_adapter.py
|   |   |-- gemini_adapter.py
|   |   |-- copilot_adapter.py
|   |   |-- ollama_adapter.py
|   |   |-- llama_cpp_adapter.py
|   |   +-- cli_communicator.py
|   |-- config/
|   |   +-- agents.yaml              #   Agents, roles, team settings
|   |-- ui/                          # Dedicated Web UI
|   |   |-- app.py                   #   Flask + Socket.IO backend
|   |   |-- frontend/                #   Nuxt 3 + Vue 3 + Tailwind
|   |   |-- static/
|   |   +-- templates/
|   +-- README.md                    #   Agentic team-specific docs
|
|-- tests/                           # Unified test suite
|   |-- conftest.py
|   |-- test_orchestrator.py
|   |-- test_adapters.py
|   |-- test_adapter_execution.py
|   |-- test_agentic_team_engine.py
|   |-- test_agentic_ui_backend.py
|   |-- test_integration.py
|   |-- test_functional_e2e.py
|   |-- test_enterprise_hardening.py
|   |-- test_production_hardening.py
|   +-- ...
|
|-- deployment/                      # Deployment configurations
|   |-- kubernetes/
|   |-- azure/
|   |-- systemd/
|   |-- load-balancer/
|   +-- scripts/
|
|-- docs/                            # Documentation
|   |-- images/                      #   Screenshots
|   |-- orchestrator-architecture.md
|   |-- orchestrator-api-reference.md
|   |-- agentic-team-architecture.md
|   |-- agentic-team-api-reference.md
|   |-- configuration-guide.md
|   |-- testing-guide.md
|   |-- security.md
|   +-- offline-mode.md
|
|-- examples/                        # Usage examples
|   |-- orchestrator/
|   +-- agentic_team/
|
|-- scripts/                         # Helper scripts
|   |-- install.sh
|   |-- start-ui.sh
|   |-- start-agentic-ui.sh
|   +-- test.sh
|
|-- ai-orchestrator                  # Main CLI entry point
|-- Dockerfile                       # Multi-stage production image
|-- docker-compose.yml               # Both UIs + monitoring stack
|-- Makefile                         # Development commands
|-- pyproject.toml                   # Project metadata and tool config
|-- requirements.txt                 # Python dependencies
|-- SETUP.md                         # Installation and setup guide
|-- ARCHITECTURE.md
|-- FEATURES.md
|-- AGENTIC_TEAM.md
|-- OFFLINE_MODE.md
|-- DEPLOYMENT.md
+-- LICENSE
```

> [!IMPORTANT]
> **Key design decision:** `orchestrator/` and `agentic_team/` are fully self-contained. Each carries its own `adapters/`, `config/`, and `ui/` directories. There are no shared root-level `adapters/`, `ui/`, or `config/` directories. The two systems share zero code and zero imports.

## Configuration

Both systems read their configuration from their own `orchestrator/config/agents.yaml` file. The files follow the same schema but are independent.

```mermaid
graph LR
    subgraph Orchestrator Config
        OC["orchestrator/config/agents.yaml"]
        OC --> OA["agents: codex, gemini, claude, ..."]
        OC --> OW["workflows: default, quick, thorough, ..."]
        OC --> OS["settings: max_iterations, output_dir, ..."]
        OC --> OAT["agentic_team: roles (shared schema)"]
    end

    subgraph Agentic Team Config
        AC["agentic_team/config/agents.yaml"]
        AC --> AA["agents: codex, gemini, claude, ..."]
        AC --> AW["workflows: (same schema)"]
        AC --> AS["settings: (same schema)"]
        AC --> AAT["agentic_team: lead_role, max_turns, roles"]
    end

    style OC fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style AC fill:#22543d,stroke:#276749,color:#e2e8f0
```

### Available Workflows

| Workflow | Pipeline | Use Case |
|---|---|---|
| `default` | Codex --> Gemini --> Claude | Production-quality code with full review |
| `quick` | Codex only | Fast prototyping |
| `thorough` | Codex --> Copilot --> Gemini --> Claude --> Gemini | Mission-critical code |
| `review-only` | Gemini --> Claude | Analyzing existing code |
| `document` | Claude --> Gemini | Documentation generation |
| `offline-default` | local-code --> local-instruct | Local-only, no cloud dependency |
| `hybrid` | local-code --> Claude (fallback: local-instruct) | Local drafts with cloud review |

## Deployment

### Docker Compose (Recommended)

Both systems are packaged in a single multi-stage Docker image. The `docker-compose.yml` runs each as a separate service.

```mermaid
graph TD
    subgraph Docker Compose
        direction TB
        OUI["orchestrator-ui<br/>:5001"]
        AUI["agentic-team-ui<br/>:5002"]
        PROM["prometheus<br/>:9091<br/>(monitoring profile)"]
        GRAF["grafana<br/>:3000<br/>(monitoring profile)"]
    end

    OUI --> SHARED_VOL["Shared Volumes<br/>output/ workspace/ logs/ sessions/"]
    AUI --> SHARED_VOL
    PROM --> OUI
    PROM --> AUI
    GRAF --> PROM

    style OUI fill:#2b6cb0,stroke:#2c5282,color:#fff
    style AUI fill:#276749,stroke:#22543d,color:#fff
    style PROM fill:#c05621,stroke:#9c4221,color:#fff
    style GRAF fill:#6b46c1,stroke:#553c9a,color:#fff
```

```bash
# Start both UIs
docker compose up --build -d

# Start with monitoring (Prometheus + Grafana)
docker compose --profile monitoring up --build -d

# Stop everything
docker compose down
```

### Kubernetes

```bash
kubectl create namespace ai-coding-tools
kubectl apply -f deployment/kubernetes/
kubectl get pods -n ai-coding-tools
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for systemd, Azure, load balancer, and production hardening guides.

## Testing

The unified test suite (314 tests across 56 modules) covers both systems independently.

```mermaid
flowchart LR
    subgraph "make all"
        FMT[format<br/>black + isort] --> LINT[lint<br/>flake8 + pylint]
        LINT --> TYPE[type-check<br/>mypy]
        TYPE --> TEST[test<br/>314 tests]
        TEST --> SEC[security<br/>bandit + safety]
    end

    subgraph "Test Targets"
        TEST --> T_ORCH[test-orchestrator]
        TEST --> T_AGENT[test-agentic]
        TEST --> T_UNIT[test-unit]
        TEST --> T_INT[test-integration]
        TEST --> T_E2E[test-e2e]
    end

    style FMT fill:#2b6cb0,stroke:#2c5282,color:#fff
    style TEST fill:#276749,stroke:#22543d,color:#fff
    style SEC fill:#9b2c2c,stroke:#742a2a,color:#fff
```

```bash
# Run all tests
make test

# Orchestrator tests only
make test-orchestrator

# Agentic team tests only
make test-agentic

# Unit tests only
make test-unit

# Integration tests only
make test-integration

# Tests with coverage report
make test-coverage
```

### Code Quality

```bash
make lint              # Lint all Python source (flake8 + pylint)
make format            # Format with black + isort
make type-check        # Run mypy on both subsystems
make security          # Run bandit + safety
make all               # Run everything (format, lint, type-check, test, security)
```

## Monitoring

Prometheus metrics are exposed by the orchestrator UI backend on port 9090.

| Metric | Description |
|---|---|
| `orchestrator_tasks_total` | Total tasks executed |
| `orchestrator_task_duration_seconds` | Task execution time |
| `orchestrator_agent_calls_total` | Agent invocations |
| `orchestrator_agent_errors_total` | Agent error count |
| `orchestrator_cache_hits_total` | Cache performance |

Health checks:
- Orchestrator: `http://localhost:5001/health`, `http://localhost:5001/ready`
- Agentic Team: `http://localhost:5002/health`, `http://localhost:5002/ready`

## Documentation

| Document | Description |
|---|---|
| **[SETUP.md](SETUP.md)** | Prerequisites, installation, environment setup, troubleshooting |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System architecture and design patterns |
| **[FEATURES.md](FEATURES.md)** | Comprehensive feature documentation |
| **[AGENTIC_TEAM.md](AGENTIC_TEAM.md)** | Agentic team runtime details |
| **[OFFLINE_MODE.md](OFFLINE_MODE.md)** | Offline mode and local model guide |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Docker, Kubernetes, systemd, Azure deployment |
| **[ADD_AGENTS.md](ADD_AGENTS.md)** | Guide for adding new AI agents |
| **[orchestrator/README.md](orchestrator/README.md)** | Orchestrator subsystem documentation |
| **[agentic_team/README.md](agentic_team/README.md)** | Agentic team subsystem documentation |
| **[docs/](docs/)** | API references, architecture deep-dives, testing guide, security |

## Screenshots

<p align="center">
  <img src="docs/images/cli.png" alt="Orchestrator CLI" width="100%"/>
</p>

<p align="center">
  <img src="docs/images/ui.png" alt="Orchestrator Web UI" width="100%"/>
</p>

<p align="center">
  <img src="docs/images/agentic-team.png" alt="Agentic Team Web UI" width="100%"/>
</p>

<p align="center">
  <img src="docs/images/cli-3.png" alt="Agentic Shell REPL" width="100%"/>
</p>

## MCP Server (Optional -- Model Context Protocol)

Both systems are optionally exposed via a [FastMCP](https://github.com/jlowin/fastmcp) server (`mcp_server/`, port 8000), letting any MCP-compatible client (Claude Desktop, other LLM agents, or custom Python scripts) drive task execution programmatically.

```bash
# Start MCP server (stdio -- for Claude Desktop integration)
python -m mcp_server.server

# Start MCP server (HTTP -- for remote clients)
python -m mcp_server.server --transport http --port 8000
```

```mermaid
graph LR
    subgraph "MCP Clients"
        CD[Claude Desktop]
        LA[LLM Agent]
        PY[Python Client]
    end

    subgraph "MCP Server :8000"
        T1[orchestrator_execute]
        T2[agentic_team_execute]
        T3[list_engines]
        T4[orchestrator_health]
        T5[agentic_team_health]
        T6[list_workflows]
        T7[list_agents]
        T8[validate_config]
        T9[team_config]
        T10[agentic_team_validate]
    end

    subgraph "Engines"
        O[Orchestrator :5001]
        A[Agentic Team :5002]
    end

    CD & LA & PY -->|MCP Protocol| T1 & T2 & T3 & T4 & T5 & T6 & T7 & T8 & T9 & T10
    T1 & T3 & T4 & T6 & T7 & T8 --> O
    T2 & T5 & T9 & T10 --> A
```

**10 MCP tools** cover task execution, agent listing, workflow listing, team config, health checks, and validation for both systems. See [`mcp_server/server.py`](mcp_server/server.py) for the full tool catalog.

> [!TIP]
> The MCP server is entirely optional. Both the Orchestrator and Agentic Team work fully via their own CLIs and Web UIs without it.

## Contributing

Contributions are welcome. Please see [CONTRIBUTING.md](.github/CONTRIBUTING.md) for guidelines.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and add tests.
4. Run checks: `make all`
5. Commit using [conventional commits](https://www.conventionalcommits.org/): `git commit -m "feat: add amazing feature"`
6. Push and open a Pull Request.

## Security

For security issues, please email security@example.com. Do not open public issues for security vulnerabilities. See [SECURITY.md](SECURITY.md) for the full security policy.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Support

- **Maintainer**: [@hoangsonww](https://github.com/hoangsonww)
- **Issues**: [GitHub Issues](https://github.com/hoangsonww/AI-Agents-Orchestrator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hoangsonww/AI-Agents-Orchestrator/discussions)

---

<div align="center">

**Made with care by [Son Nguyen](https://github.com/hoangsonww) for the AI development community**

[Back to Top](#ai-coding-tools)

</div>
