#!/usr/bin/env python3
"""Seed both context graphs with rich, realistic development data.

Usage:
    python scripts/seed_context_graphs.py                        # Seed both systems
    python scripts/seed_context_graphs.py --system orchestrator  # Seed only orchestrator
    python scripts/seed_context_graphs.py --system agentic_team  # Seed only agentic team
    python scripts/seed_context_graphs.py --force                # Re-seed even if data exists
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure project root is on sys.path regardless of working directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

SEED_MARKER_TITLE = "Task: JWT Authentication Implementation"


# ---------------------------------------------------------------------------
# Orchestrator seeding
# ---------------------------------------------------------------------------


def _check_orchestrator_seeded(manager) -> bool:
    """Return True if the orchestrator graph already contains seed data."""
    from orchestrator.context.models.schemas import NodeType

    nodes = manager.graph_store.query_nodes(node_type=NodeType.TASK, limit=200)
    return any(n.title == SEED_MARKER_TITLE for n in nodes)


def seed_orchestrator(force: bool = False) -> dict[str, int]:
    """Populate the orchestrator context graph with realistic data.

    Returns a summary dict with counts of created entities.
    """
    try:
        from orchestrator.context import MemoryManager
        from orchestrator.context.models.schemas import EdgeType
    except ImportError as exc:
        print(f"  ⚠  Orchestrator context module unavailable: {exc}")
        return {}

    mgr = MemoryManager()
    summary: dict[str, int] = {
        "tasks": 0,
        "mistakes": 0,
        "patterns": 0,
        "decisions": 0,
        "conversations": 0,
        "edges": 0,
    }
    try:
        if not force and _check_orchestrator_seeded(mgr):
            print("  ✓  Orchestrator graph already seeded — skipping (use --force to re-seed)")
            return summary

        # ── Tasks (10) ────────────────────────────────────────────────
        t1 = mgr.store_task(
            task_description="JWT Authentication Implementation",
            outcome="Implemented JWT-based auth with access/refresh tokens, bcrypt password hashing, "
            "and role-based access control. Added /auth/login, /auth/refresh, /auth/logout endpoints.",
            success=True,
            duration_ms=14400000,
            agents_involved=["claude", "codex"],
            tags=["auth", "security", "api"],
        )
        t2 = mgr.store_task(
            task_description="PostgreSQL query optimization for analytics dashboard",
            outcome="Reduced p95 query latency from 4.2s to 180ms by adding composite indexes, "
            "rewriting N+1 queries to batch SELECTs, and enabling pg_stat_statements monitoring.",
            success=True,
            duration_ms=7200000,
            agents_involved=["claude", "gemini"],
            tags=["database", "performance", "postgres"],
        )
        t3 = mgr.store_task(
            task_description="Kubernetes deployment manifest creation",
            outcome="Created Helm chart with Deployment, Service, Ingress, HPA, PDB, and "
            "NetworkPolicy resources. Configured liveness/readiness probes and resource limits.",
            success=True,
            duration_ms=5400000,
            agents_involved=["copilot"],
            tags=["devops", "kubernetes", "deployment"],
        )
        t4 = mgr.store_task(  # noqa: F841
            task_description="React component library with Storybook",
            outcome="Built 24 accessible UI components (Button, Modal, DataTable, Toast, etc.) "
            "with Storybook stories, Jest tests at 92% coverage, and Chromatic visual regression.",
            success=True,
            duration_ms=28800000,
            agents_involved=["claude", "copilot"],
            tags=["frontend", "react", "components"],
        )
        t5 = mgr.store_task(  # noqa: F841
            task_description="CI/CD pipeline migration from Jenkins to GitHub Actions",
            outcome="FAILED: Migrated 12 of 15 pipelines successfully but the integration test "
            "workflow timed out due to missing self-hosted runner labels. Rollback to Jenkins "
            "for remaining 3 pipelines.",
            success=False,
            duration_ms=18000000,
            agents_involved=["codex", "gemini"],
            tags=["ci-cd", "github-actions", "migration"],
        )
        t6 = mgr.store_task(
            task_description="ML inference API with FastAPI and ONNX Runtime",
            outcome="Deployed a FastAPI service wrapping an ONNX-optimized sentiment analysis model. "
            "Achieves 12ms p50 latency, 45ms p99 under 500 RPS. Includes batch endpoint.",
            success=True,
            duration_ms=10800000,
            agents_involved=["claude", "ollama"],
            tags=["ml", "inference", "fastapi"],
        )
        t7 = mgr.store_task(
            task_description="Security audit and penetration testing",
            outcome="FAILED: Discovered 3 critical vulnerabilities — SQL injection in search endpoint, "
            "exposed admin panel without auth, and hardcoded AWS credentials in .env.example. "
            "Remediation plan created.",
            success=False,
            duration_ms=21600000,
            agents_involved=["claude", "gemini"],
            tags=["security", "audit", "pentest"],
        )
        t8 = mgr.store_task(
            task_description="Event-driven microservices with RabbitMQ",
            outcome="Implemented order processing pipeline: OrderCreated → PaymentProcessed → "
            "InventoryReserved → ShipmentScheduled. Dead-letter queues for failure handling.",
            success=True,
            duration_ms=16200000,
            agents_involved=["claude", "codex"],
            tags=["microservices", "rabbitmq", "events"],
        )
        t9 = mgr.store_task(
            task_description="Prometheus and Grafana monitoring stack",
            outcome="Deployed full observability stack: Prometheus for metrics, Grafana for dashboards, "
            "Alertmanager for PagerDuty integration. Created 8 alert rules covering SLOs.",
            success=True,
            duration_ms=9000000,
            agents_involved=["copilot"],
            tags=["monitoring", "prometheus", "grafana"],
        )
        t10 = mgr.store_task(
            task_description="Database migration from MongoDB to PostgreSQL",
            outcome="FAILED: Data migration script crashed at 68% due to UTF-8 encoding issues in "
            "legacy documents. Partial rollback completed; need to sanitize source data first.",
            success=False,
            duration_ms=25200000,
            agents_involved=["claude", "codex", "gemini"],
            tags=["database", "migration", "postgres"],
        )
        summary["tasks"] = 10

        # ── Mistakes (8) ──────────────────────────────────────────────
        m1 = mgr.log_mistake(
            error_type="sql_injection",
            error_message="Unsanitized user input concatenated into SQL WHERE clause in /api/search",
            context_description="Search endpoint used f-string interpolation instead of parameterized queries",
            correction="Replaced f-string SQL with parameterized query using ? placeholders",
            prevention_strategy="Always use ORM query builders or parameterized queries; add SQLi detection to CI linter",
            severity="critical",
            tags=["security", "sql", "injection"],
            related_task_id=t7,
        )
        m2 = mgr.log_mistake(  # noqa: F841
            error_type="memory_leak",
            error_message="Node.js EventEmitter listener leak — 847 listeners attached to 'data' event",
            context_description="WebSocket handler registered new listeners on each connection without cleanup",
            correction="Added removeListener in socket 'close' handler; implemented listener cap with setMaxListeners",
            prevention_strategy="Use once() for single-fire events; always pair addEventListener with removeEventListener",
            severity="high",
            tags=["performance", "nodejs", "memory"],
        )
        m3 = mgr.log_mistake(
            error_type="race_condition",
            error_message="Duplicate order creation under concurrent requests — inventory decremented twice",
            context_description="Two concurrent POST /orders for the same item passed stock check simultaneously",
            correction="Added SELECT ... FOR UPDATE row-level lock in the inventory check transaction",
            prevention_strategy="Use pessimistic locking or optimistic concurrency control with version columns for inventory",
            severity="critical",
            tags=["concurrency", "database", "orders"],
        )
        m4 = mgr.log_mistake(
            error_type="missing_index",
            error_message="Full table scan on users.email during login — 12s query time on 5M rows",
            context_description="Login endpoint queried users by email without a database index",
            correction="Created UNIQUE index on users(email) — query dropped to 0.3ms",
            prevention_strategy="Run EXPLAIN ANALYZE on all new queries; add index review to PR checklist",
            severity="high",
            tags=["database", "performance", "indexing"],
            related_task_id=t2,
        )
        m5 = mgr.log_mistake(
            error_type="exposed_secrets",
            error_message="AWS_SECRET_ACCESS_KEY committed to .env.example in public repository",
            context_description="Developer copied real .env to .env.example and forgot to redact credentials",
            correction="Rotated AWS keys immediately; removed file from git history with git filter-branch",
            prevention_strategy="Add pre-commit hook with detect-secrets; never use real credentials in example files",
            severity="critical",
            tags=["security", "secrets", "aws"],
            related_task_id=t7,
        )
        m6 = mgr.log_mistake(
            error_type="cors_misconfiguration",
            error_message="Access-Control-Allow-Origin set to * in production — allows any origin",
            context_description="CORS middleware left in development mode after deployment",
            correction="Restricted allowed origins to specific production domains; added environment-based CORS config",
            prevention_strategy="Use environment-specific CORS configs; add security header checks to CI pipeline",
            severity="medium",
            tags=["security", "cors", "api"],
        )
        m7 = mgr.log_mistake(
            error_type="n_plus_one_query",
            error_message="Dashboard loaded 200 users then issued 200 individual queries for their orders",
            context_description="ORM lazy loading fetched related orders one-by-one in a template loop",
            correction="Used eager loading with joinedload() to fetch users and orders in a single query",
            prevention_strategy="Enable SQLAlchemy warn_on_lazy_load in dev; review query logs for repeated patterns",
            severity="medium",
            tags=["database", "performance", "orm"],
            related_task_id=t2,
        )
        m8 = mgr.log_mistake(
            error_type="certificate_expiry",
            error_message="TLS certificate expired causing 2-hour production outage on api.example.com",
            context_description="Manual cert renewal process missed renewal deadline by 3 days",
            correction="Installed cert-manager in Kubernetes with Let's Encrypt auto-renewal",
            prevention_strategy="Use automated certificate management; set up 30/14/7-day expiry alerts in monitoring",
            severity="high",
            tags=["devops", "tls", "outage"],
        )
        summary["mistakes"] = 8

        # ── Patterns (8) ─────────────────────────────────────────────
        p1 = mgr.store_pattern(
            pattern_name="Repository Pattern",
            pattern_type="architecture",
            description="Abstract data access behind a repository interface to decouple business logic "
            "from persistence. Each aggregate root gets its own repository with CRUD + query methods.",
            examples=[
                "class UserRepository(ABC):\n    @abstractmethod\n    def find_by_email(self, email: str) -> User | None: ...\n    @abstractmethod\n    def save(self, user: User) -> None: ...",
            ],
            anti_patterns=[
                "Direct SQL in route handlers",
                "ORM queries scattered across business logic",
            ],
            languages=["python", "typescript"],
            frameworks=["fastapi", "django", "express"],
            tags=["pattern", "architecture", "repository"],
        )
        p2 = mgr.store_pattern(
            pattern_name="Circuit Breaker",
            pattern_type="resilience",
            description="Prevent cascading failures by wrapping external service calls in a circuit breaker "
            "that trips after N consecutive failures, returning a fallback for a cooldown period.",
            examples=[
                "from circuitbreaker import circuit\n\n@circuit(failure_threshold=5, recovery_timeout=30)\ndef call_payment_api(order_id: str) -> PaymentResult:\n    return requests.post(PAYMENT_URL, json={...}).json()",
            ],
            anti_patterns=["Unbounded retries without backoff", "No timeout on HTTP calls"],
            languages=["python", "java"],
            frameworks=["resilience4j", "pybreaker"],
            tags=["pattern", "resilience", "circuit-breaker"],
        )
        p3 = mgr.store_pattern(
            pattern_name="Retry with Exponential Backoff",
            pattern_type="resilience",
            description="Retry transient failures with increasing delays (1s, 2s, 4s, 8s…) plus jitter "
            "to prevent thundering herd. Cap at max_retries and max_delay.",
            examples=[
                "from tenacity import retry, stop_after_attempt, wait_exponential\n\n@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, max=60))\ndef fetch_data(url: str) -> dict:\n    resp = requests.get(url, timeout=10)\n    resp.raise_for_status()\n    return resp.json()",
            ],
            anti_patterns=[
                "Fixed-interval retries",
                "Retrying non-idempotent operations without dedup",
            ],
            languages=["python", "typescript"],
            tags=["pattern", "resilience", "retry"],
        )
        p4 = mgr.store_pattern(
            pattern_name="Event Sourcing",
            pattern_type="architecture",
            description="Persist domain events as the source of truth instead of mutable state. "
            "Rebuild current state by replaying the event stream. Enables audit trails and temporal queries.",
            examples=[
                "class OrderEventStore:\n    def append(self, order_id: str, event: DomainEvent) -> None: ...\n    def get_events(self, order_id: str) -> list[DomainEvent]: ...\n    def rebuild_state(self, order_id: str) -> Order:\n        events = self.get_events(order_id)\n        return reduce(apply_event, events, Order())",
            ],
            anti_patterns=["Mutable state without audit log", "Deleting events from the store"],
            languages=["python", "java", "csharp"],
            tags=["pattern", "architecture", "event-sourcing"],
        )
        p5 = mgr.store_pattern(
            pattern_name="Feature Flags",
            pattern_type="devops",
            description="Decouple deployment from release by wrapping new features behind toggles. "
            "Supports canary rollouts, A/B testing, and instant kill switches.",
            examples=[
                "if feature_flags.is_enabled('new-checkout-flow', user_id=request.user.id):\n    return render_new_checkout()\nelse:\n    return render_legacy_checkout()",
            ],
            anti_patterns=[
                "Long-lived flags never cleaned up",
                "Flag logic deeply nested in business code",
            ],
            languages=["python", "typescript", "go"],
            frameworks=["launchdarkly", "unleash", "flipt"],
            tags=["pattern", "devops", "feature-flags"],
        )
        p6 = mgr.store_pattern(
            pattern_name="Health Check Endpoint",
            pattern_type="api",
            description="Expose /healthz (liveness) and /readyz (readiness) endpoints that verify "
            "database connectivity, cache availability, and downstream dependency status.",
            examples=[
                "@app.get('/healthz')\nasync def healthz():\n    return {'status': 'ok'}\n\n@app.get('/readyz')\nasync def readyz():\n    db_ok = await check_db()\n    cache_ok = await check_redis()\n    return {'ready': db_ok and cache_ok, 'checks': {'db': db_ok, 'cache': cache_ok}}",
            ],
            anti_patterns=[
                "Health endpoint that always returns 200",
                "Heavy computation in health checks",
            ],
            languages=["python", "go"],
            frameworks=["fastapi", "express", "gin"],
            tags=["pattern", "api", "health-check"],
        )
        p7 = mgr.store_pattern(
            pattern_name="Structured Logging",
            pattern_type="observability",
            description="Emit logs as structured JSON with consistent fields (timestamp, level, service, "
            "trace_id, message). Enables log aggregation, searching, and correlation.",
            examples=[
                'import structlog\n\nlog = structlog.get_logger()\nlog.info("order_created", order_id=order.id, amount=order.total, user_id=user.id)',
            ],
            anti_patterns=[
                "Unstructured print() statements",
                "Logging sensitive data (passwords, tokens)",
            ],
            languages=["python", "go", "typescript"],
            frameworks=["structlog", "zap", "pino"],
            tags=["pattern", "observability", "logging"],
        )
        p8 = mgr.store_pattern(
            pattern_name="Input Validation with Pydantic",
            pattern_type="security",
            description="Validate and coerce all API inputs at the boundary using Pydantic models. "
            "Reject malformed data before it reaches business logic.",
            examples=[
                "from pydantic import BaseModel, EmailStr, constr\n\nclass CreateUserRequest(BaseModel):\n    email: EmailStr\n    name: constr(min_length=1, max_length=100)\n    password: constr(min_length=8)",
            ],
            anti_patterns=["Manual dict key checking", "Trusting client-side validation"],
            languages=["python"],
            frameworks=["pydantic", "fastapi"],
            tags=["pattern", "security", "validation"],
        )
        summary["patterns"] = 8

        # ── Decisions (5) ─────────────────────────────────────────────
        d1 = mgr.store_decision(
            decision_title="Adopt PostgreSQL over MongoDB for primary datastore",
            decision_description="Replace MongoDB with PostgreSQL as the primary database for "
            "transactional workloads requiring strong consistency and complex queries.",
            rationale="Our data model is heavily relational with many joins. PostgreSQL provides ACID "
            "transactions, mature indexing (GIN, GiST), JSONB for flexible fields, and "
            "excellent query planner. MongoDB's document model led to data duplication issues.",
            alternatives_considered=["MongoDB (current)", "CockroachDB", "MySQL 8"],
            trade_offs="Requires data migration effort; team needs PostgreSQL training; "
            "lose MongoDB's flexible schema for rapid prototyping",
            status="accepted",
            tags=["decision", "database", "postgres"],
        )
        d2 = mgr.store_decision(
            decision_title="Use FastAPI for new Python microservices",
            decision_description="Standardize on FastAPI as the web framework for all new Python services, "
            "replacing Flask.",
            rationale="FastAPI provides automatic OpenAPI docs, native async support, Pydantic validation, "
            "and significantly better performance than Flask. Type hints enable IDE autocompletion "
            "and catch errors at development time.",
            alternatives_considered=["Flask (current)", "Django REST Framework", "Starlette"],
            trade_offs="Team must learn async Python patterns; existing Flask services remain until "
            "natural migration points",
            status="accepted",
            tags=["decision", "framework", "fastapi"],
        )
        d3 = mgr.store_decision(
            decision_title="Multi-region Kubernetes deployment on AWS EKS",
            decision_description="Deploy application across us-east-1 and eu-west-1 EKS clusters with "
            "global load balancing for <100ms latency worldwide.",
            rationale="User base is 40% US, 35% EU. Single-region deployment causes 200ms+ latency for "
            "EU users. EKS provides managed control plane, and our team already has Kubernetes expertise.",
            alternatives_considered=["Single-region with CDN", "AWS ECS Fargate", "Google GKE"],
            trade_offs="Higher infrastructure cost (~40%); increased operational complexity; "
            "need cross-region database replication strategy",
            status="accepted",
            tags=["decision", "infrastructure", "kubernetes", "aws"],
        )
        d4 = mgr.store_decision(
            decision_title="Event-driven architecture with RabbitMQ",
            decision_description="Adopt event-driven architecture using RabbitMQ for inter-service "
            "communication instead of synchronous REST calls.",
            rationale="Synchronous REST calls created tight coupling and cascading failures. "
            "RabbitMQ provides reliable message delivery, dead-letter exchanges, and "
            "decouples producers from consumers.",
            alternatives_considered=["Apache Kafka", "AWS SQS/SNS", "Redis Streams", "NATS"],
            trade_offs="Added infrastructure complexity; eventual consistency requires careful handling; "
            "debugging distributed flows is harder than synchronous calls",
            status="accepted",
            tags=["decision", "architecture", "messaging"],
        )
        d5 = mgr.store_decision(  # noqa: F841
            decision_title="Monorepo with Turborepo for frontend packages",
            decision_description="Consolidate frontend packages (UI library, shared utils, app shells) "
            "into a single monorepo managed by Turborepo.",
            rationale="Separate repos caused version drift between shared packages. Turborepo provides "
            "incremental builds, remote caching, and task orchestration. Developers can make "
            "cross-package changes in a single PR.",
            alternatives_considered=["Separate repos with npm link", "Nx", "Lerna", "Bazel"],
            trade_offs="Larger repo size; CI runs need smart filtering; onboarding requires "
            "understanding of workspace structure",
            status="accepted",
            tags=["decision", "frontend", "monorepo", "tooling"],
        )
        summary["decisions"] = 5

        # ── Conversations (4) ─────────────────────────────────────────
        c1 = mgr.store_conversation(
            messages=[
                {
                    "role": "user",
                    "content": "We're seeing intermittent 504 errors on the /api/orders endpoint during peak hours. Load is about 2000 RPM.",
                },
                {
                    "role": "claude",
                    "content": "Let me analyze the error pattern. The 504s suggest upstream timeout. I'll check the database connection pool, the order service's thread pool, and downstream payment API latency.",
                },
                {
                    "role": "user",
                    "content": "Good call — the payment API has been slow lately. Average response time jumped from 200ms to 1.8s.",
                },
                {
                    "role": "claude",
                    "content": "That explains it. Your order service has a 2s timeout and the payment API is flirting with that limit under load. I recommend: 1) Add a circuit breaker around the payment call, 2) Increase the timeout to 5s with a 3-retry backoff, 3) Consider async payment processing with a webhook callback.",
                },
                {
                    "role": "user",
                    "content": "Let's go with the circuit breaker approach. Can you implement it?",
                },
                {
                    "role": "claude",
                    "content": "Done. I've wrapped the payment call with pybreaker (threshold=5 failures, reset_timeout=30s). Added a fallback that queues the payment for retry via RabbitMQ. Also added Prometheus metrics for circuit state changes.",
                },
            ],
            summary="Debugging 504 errors on /api/orders caused by slow payment API; implemented circuit breaker",
            session_id="session-orch-001",
            participants=["user", "claude"],
            tags=["debugging", "performance", "circuit-breaker"],
        )
        c2 = mgr.store_conversation(
            messages=[
                {
                    "role": "user",
                    "content": "Our security scan flagged a potential SQL injection in the search endpoint. Can you audit the codebase?",
                },
                {
                    "role": "claude",
                    "content": "I found 3 instances of unsafe SQL construction:\n1. /api/search uses f-string interpolation for the WHERE clause\n2. /api/reports builds ORDER BY from user input without validation\n3. /admin/users concatenates filter params directly into SQL",
                },
                {
                    "role": "gemini",
                    "content": "I've also detected that the admin panel at /admin has no authentication middleware. It's accessible to anyone who knows the URL.",
                },
                {
                    "role": "user",
                    "content": "Critical. Let's fix all of these immediately. Prioritize the SQL injection issues.",
                },
                {
                    "role": "claude",
                    "content": "All three SQL injection vulnerabilities are now patched using parameterized queries. I've also added an allow-list for ORDER BY columns and a security middleware for the admin panel requiring JWT with admin role.",
                },
            ],
            summary="Security audit discovered SQL injection and unprotected admin panel; all issues remediated",
            session_id="session-orch-002",
            participants=["user", "claude", "gemini"],
            tags=["security", "audit", "sql-injection"],
        )
        c3 = mgr.store_conversation(
            messages=[
                {
                    "role": "user",
                    "content": "We need to migrate our database from MongoDB to PostgreSQL. What's the plan?",
                },
                {
                    "role": "claude",
                    "content": "I suggest a phased approach:\n1. Schema design — map MongoDB collections to relational tables\n2. Migration script — use a dual-write pattern during transition\n3. Validation — compare record counts and checksums\n4. Cutover — switch reads to PostgreSQL, then disable MongoDB writes",
                },
                {
                    "role": "user",
                    "content": "The migration script crashed at 68% with a UnicodeDecodeError. What happened?",
                },
                {
                    "role": "claude",
                    "content": "The legacy MongoDB data contains documents with invalid UTF-8 sequences from a 2019 encoding bug. We need to add a sanitization pass: decode with errors='replace', log affected document IDs, and verify with stakeholders before proceeding.",
                },
            ],
            summary="Planning and troubleshooting MongoDB to PostgreSQL migration; encoding issues discovered",
            session_id="session-orch-003",
            participants=["user", "claude"],
            tags=["database", "migration", "postgres"],
        )
        c4 = mgr.store_conversation(
            messages=[
                {
                    "role": "user",
                    "content": "Can you help set up our monitoring stack? We have zero observability right now.",
                },
                {
                    "role": "copilot",
                    "content": "I'll set up a full observability stack:\n- Prometheus for metrics collection\n- Grafana for dashboards and visualization\n- Alertmanager for PagerDuty integration\n- Loki for log aggregation",
                },
                {"role": "user", "content": "What SLO-based alerts should we configure?"},
                {
                    "role": "copilot",
                    "content": "Based on your API traffic patterns, I recommend these alert rules:\n1. Error rate > 1% over 5min window (P1)\n2. p99 latency > 2s for 10min (P2)\n3. Successful request rate drops > 30% vs previous hour (P1)\n4. Pod restart count > 3 in 15min (P2)\n5. Disk usage > 80% (P3)\n6. Certificate expiry < 14 days (P2)",
                },
            ],
            summary="Setting up Prometheus/Grafana monitoring stack with SLO-based alerting",
            session_id="session-orch-004",
            participants=["user", "copilot"],
            tags=["monitoring", "observability", "alerting"],
        )
        summary["conversations"] = 4

        # ── Edges (28) ────────────────────────────────────────────────
        edges = [
            # Mistake → Task (CAUSED_BY) — mistakes discovered during tasks
            (
                m1,
                t7,
                EdgeType.CAUSED_BY,
                1.0,
                {"context": "SQL injection found during security audit"},
            ),
            (
                m5,
                t7,
                EdgeType.CAUSED_BY,
                1.0,
                {"context": "Exposed secrets found during security audit"},
            ),
            (
                m4,
                t2,
                EdgeType.CAUSED_BY,
                0.9,
                {"context": "Missing index found during query optimization"},
            ),
            (
                m7,
                t2,
                EdgeType.CAUSED_BY,
                0.9,
                {"context": "N+1 query found during optimization work"},
            ),
            # Pattern → Mistake (FIXED_BY) — patterns that fix mistakes
            (
                p8,
                m1,
                EdgeType.FIXED_BY,
                1.0,
                {"context": "Input validation prevents injection attacks"},
            ),
            (
                p2,
                m3,
                EdgeType.FIXED_BY,
                0.9,
                {"context": "Circuit breaker prevents cascading failures from race conditions"},
            ),
            (
                p1,
                m7,
                EdgeType.FIXED_BY,
                0.8,
                {"context": "Repository pattern centralizes query logic, preventing N+1"},
            ),
            # Task → Task (PRECEDED_BY)
            (
                t2,
                t10,
                EdgeType.PRECEDED_BY,
                0.8,
                {"context": "Query optimization informed migration approach"},
            ),
            (
                t7,
                t1,
                EdgeType.PRECEDED_BY,
                0.9,
                {"context": "Security audit preceded auth implementation hardening"},
            ),
            (
                t9,
                t3,
                EdgeType.PRECEDED_BY,
                0.7,
                {"context": "Monitoring setup preceded K8s deployment refinement"},
            ),
            # Decision → Task (USED_IN)
            (
                d1,
                t2,
                EdgeType.USED_IN,
                1.0,
                {"context": "PostgreSQL decision drove query optimization task"},
            ),
            (
                d1,
                t10,
                EdgeType.USED_IN,
                1.0,
                {"context": "PostgreSQL decision initiated migration task"},
            ),
            (
                d2,
                t6,
                EdgeType.USED_IN,
                0.9,
                {"context": "FastAPI decision applied in ML inference service"},
            ),
            (
                d3,
                t3,
                EdgeType.USED_IN,
                0.9,
                {"context": "EKS decision drove K8s manifest creation"},
            ),
            (
                d4,
                t8,
                EdgeType.USED_IN,
                1.0,
                {"context": "RabbitMQ decision implemented in event microservices"},
            ),
            # Pattern → Decision (REFERENCES)
            (
                p2,
                d4,
                EdgeType.REFERENCES,
                0.8,
                {"context": "Circuit breaker pattern referenced in messaging decision"},
            ),
            (
                p4,
                d4,
                EdgeType.REFERENCES,
                0.9,
                {"context": "Event sourcing pattern referenced in architecture decision"},
            ),
            (
                p6,
                d3,
                EdgeType.REFERENCES,
                0.7,
                {"context": "Health check pattern referenced in K8s deployment decision"},
            ),
            # Similar patterns
            (
                p2,
                p3,
                EdgeType.SIMILAR_TO,
                0.9,
                {"context": "Both are resilience patterns for external calls"},
            ),
            (
                p1,
                p4,
                EdgeType.SIMILAR_TO,
                0.7,
                {"context": "Both are data access architecture patterns"},
            ),
            # Conversations → Tasks (RELATED_TO)
            (
                c1,
                t8,
                EdgeType.RELATED_TO,
                0.8,
                {"context": "504 debugging led to event-driven implementation"},
            ),
            (
                c2,
                t7,
                EdgeType.RELATED_TO,
                1.0,
                {"context": "Security audit conversation directly tied to task"},
            ),
            (
                c3,
                t10,
                EdgeType.RELATED_TO,
                1.0,
                {"context": "Migration discussion tied to migration task"},
            ),
            (
                c4,
                t9,
                EdgeType.RELATED_TO,
                1.0,
                {"context": "Monitoring setup conversation tied to task"},
            ),
            # LEARNED_FROM — mistakes that led to patterns
            (
                p7,
                m8,
                EdgeType.LEARNED_FROM,
                0.8,
                {
                    "context": "Structured logging adopted after certificate outage diagnosis was hampered"
                },
            ),
            (
                p5,
                m6,
                EdgeType.LEARNED_FROM,
                0.7,
                {"context": "Feature flags adopted after CORS misconfiguration in prod"},
            ),
            # Task → Pattern (USED_IN)
            (
                p2,
                t8,
                EdgeType.USED_IN,
                0.9,
                {"context": "Circuit breaker pattern used in microservices task"},
            ),
            (
                p6,
                t3,
                EdgeType.USED_IN,
                0.8,
                {"context": "Health check pattern used in K8s deployment"},
            ),
        ]

        for src, tgt, etype, weight, meta in edges:
            mgr.link_nodes(
                source_id=src,
                target_id=tgt,
                edge_type=etype,
                weight=weight,
                metadata=meta,
            )
        summary["edges"] = len(edges)

    finally:
        mgr.close()

    return summary


# ---------------------------------------------------------------------------
# Agentic Team seeding
# ---------------------------------------------------------------------------


def _check_agentic_seeded(manager) -> bool:
    """Return True if the agentic team graph already contains seed data."""
    from agentic_team.context.models.schemas import NodeType

    nodes = manager.graph_store.query_nodes(node_type=NodeType.TASK, limit=200)
    return any(n.title == SEED_MARKER_TITLE for n in nodes)


def seed_agentic_team(force: bool = False) -> dict[str, int]:
    """Populate the agentic team context graph with realistic data.

    Returns a summary dict with counts of created entities.
    """
    try:
        from agentic_team.context import MemoryManager
        from agentic_team.context.models.schemas import EdgeType
    except ImportError as exc:
        print(f"  ⚠  Agentic team context module unavailable: {exc}")
        return {}

    mgr = MemoryManager()
    summary: dict[str, int] = {
        "tasks": 0,
        "mistakes": 0,
        "patterns": 0,
        "decisions": 0,
        "conversations": 0,
        "edges": 0,
    }
    try:
        if not force and _check_agentic_seeded(mgr):
            print("  ✓  Agentic team graph already seeded — skipping (use --force to re-seed)")
            return summary

        # ── Tasks (10) ────────────────────────────────────────────────
        t1 = mgr.store_task(
            task_description="JWT Authentication Implementation",
            outcome="Built JWT auth module with access/refresh token rotation, bcrypt hashing, "
            "and RBAC middleware. Integrated with existing FastAPI user service.",
            success=True,
            duration_ms=12600000,
            agents_involved=["claude", "copilot"],
            tags=["auth", "security", "jwt"],
        )
        t2 = mgr.store_task(
            task_description="GraphQL API gateway with Apollo Federation",
            outcome="Implemented federated GraphQL gateway stitching 4 subgraphs (users, products, "
            "orders, inventory). Added DataLoader for N+1 prevention and Redis query caching.",
            success=True,
            duration_ms=19800000,
            agents_involved=["claude", "codex"],
            tags=["api", "graphql", "federation"],
        )
        t3 = mgr.store_task(  # noqa: F841
            task_description="Docker multi-stage build optimization",
            outcome="Reduced Docker image from 1.8GB to 142MB using multi-stage builds, Alpine base, "
            "and .dockerignore. Build time dropped from 8min to 90sec with layer caching.",
            success=True,
            duration_ms=3600000,
            agents_involved=["copilot"],
            tags=["devops", "docker", "optimization"],
        )
        t4 = mgr.store_task(
            task_description="End-to-end test suite with Playwright",
            outcome="Created 87 E2E tests covering critical user flows (signup, checkout, dashboard). "
            "Integrated with GitHub Actions using sharded parallel execution across 4 workers.",
            success=True,
            duration_ms=14400000,
            agents_involved=["claude", "gemini"],
            tags=["testing", "e2e", "playwright"],
        )
        t5 = mgr.store_task(
            task_description="Redis cluster setup for session management",
            outcome="FAILED: Redis Cluster deployment hit split-brain during network partition test. "
            "Sentinel mode chosen as fallback for our scale (< 50GB dataset).",
            success=False,
            duration_ms=10800000,
            agents_involved=["codex"],
            tags=["infrastructure", "redis", "caching"],
        )
        t6 = mgr.store_task(
            task_description="OpenTelemetry distributed tracing integration",
            outcome="Instrumented 6 microservices with OpenTelemetry SDK. Traces exported to Jaeger "
            "via OTLP collector. Added custom spans for database queries and external API calls.",
            success=True,
            duration_ms=7200000,
            agents_involved=["claude", "copilot"],
            tags=["observability", "tracing", "opentelemetry"],
        )
        t7 = mgr.store_task(  # noqa: F841
            task_description="Automated database backup and disaster recovery",
            outcome="Set up WAL-G continuous archiving to S3 with point-in-time recovery. "
            "Tested recovery to within 5 seconds of any point in the last 30 days.",
            success=True,
            duration_ms=5400000,
            agents_involved=["gemini"],
            tags=["database", "backup", "disaster-recovery"],
        )
        t8 = mgr.store_task(
            task_description="WebSocket real-time notification system",
            outcome="FAILED: Initial implementation with Socket.IO hit 10K connection limit due to "
            "sticky sessions requirement. Redesigning with SSE + Redis pub/sub for stateless scaling.",
            success=False,
            duration_ms=16200000,
            agents_involved=["claude", "codex"],
            tags=["realtime", "websocket", "notifications"],
        )
        t9 = mgr.store_task(
            task_description="API rate limiting with sliding window",
            outcome="Implemented sliding window rate limiter using Redis sorted sets. Supports "
            "per-user, per-IP, and per-endpoint limits. Returns X-RateLimit-* headers.",
            success=True,
            duration_ms=4500000,
            agents_involved=["claude"],
            tags=["api", "rate-limiting", "security"],
        )
        t10 = mgr.store_task(
            task_description="Terraform infrastructure-as-code for AWS",
            outcome="FAILED: Terraform apply destroyed production RDS instance due to missing "
            "prevent_destroy lifecycle rule. Restored from snapshot with 45min downtime.",
            success=False,
            duration_ms=28800000,
            agents_involved=["codex", "gemini"],
            tags=["infrastructure", "terraform", "aws"],
        )
        summary["tasks"] = 10

        # ── Mistakes (8) ──────────────────────────────────────────────
        m1 = mgr.log_mistake(
            error_description="GraphQL query depth exploit allowed unbounded nested queries consuming "
            "100% CPU — query: { users { orders { items { product { reviews { ... } } } } } }",
            context="GraphQL gateway had no query depth or complexity limits configured",
            correction="Added graphql-depth-limit (max depth=7) and graphql-query-complexity "
            "(max cost=1000) middleware",
            prevention="Always configure query depth limits and complexity analysis for GraphQL APIs",
            category="security",
            severity="critical",
        )
        m2 = mgr.log_mistake(
            error_description="Terraform destroy deleted production RDS instance — 45 minutes of downtime "
            "before snapshot restore completed",
            context="Terraform plan showed 'destroy and recreate' for RDS but operator approved without reading",
            correction="Added lifecycle { prevent_destroy = true } to all stateful resources; "
            "implemented mandatory terraform plan review in CI",
            prevention="Use prevent_destroy on stateful resources; require plan approval in CI; "
            "separate stateful/stateless Terraform state files",
            category="infrastructure",
            severity="critical",
        )
        m3 = mgr.log_mistake(  # noqa: F841
            error_description="Docker container ran as root in production allowing container escape "
            "vulnerability via CVE-2024-21626",
            context="Dockerfile did not specify USER directive; default is root",
            correction="Added non-root user to Dockerfile: RUN adduser --system --no-create-home appuser "
            "and USER appuser",
            prevention="Add USER directive to all Dockerfiles; scan with Trivy in CI; "
            "enforce PodSecurityPolicy in Kubernetes",
            category="security",
            severity="critical",
        )
        m4 = mgr.log_mistake(
            error_description="WebSocket connection leak — server accumulated 50K stale connections "
            "over 72 hours, exhausting file descriptors",
            context="Socket.IO disconnect event handler had a try/except that silently swallowed "
            "cleanup errors",
            correction="Fixed error handling in disconnect; added connection timeout (idle > 5min); "
            "implemented connection count metrics",
            prevention="Monitor open connection counts; set idle timeouts; never silently swallow "
            "exceptions in cleanup handlers",
            category="performance",
            severity="high",
        )
        m5 = mgr.log_mistake(
            error_description="JWT tokens had no expiration — stolen token granted permanent access",
            context="Token generation code set exp claim to None for 'convenience' during development",
            correction="Set access token expiry to 15min, refresh token to 7 days; added token "
            "revocation via Redis blacklist",
            prevention="Never disable security features in dev; use short-lived tokens; "
            "implement token rotation",
            category="security",
            severity="critical",
        )
        m6 = mgr.log_mistake(  # noqa: F841
            error_description="Playwright tests flaky due to hardcoded 2-second waits instead of "
            "proper element selectors",
            context="E2E tests used page.waitForTimeout(2000) instead of waiting for specific elements",
            correction="Replaced all waitForTimeout with waitForSelector, waitForResponse, and "
            "expect(locator).toBeVisible()",
            prevention="Ban waitForTimeout in test linter rules; use auto-waiting locators; "
            "add flakiness detection to CI",
            category="testing",
            severity="medium",
        )
        m7 = mgr.log_mistake(
            error_description="Redis connection pool exhaustion caused cascading timeouts across "
            "all microservices sharing the pool",
            context="All 6 services shared a single Redis connection pool with max_connections=10",
            correction="Gave each service its own Redis connection pool; increased max_connections "
            "to 50 per service; added connection pool monitoring",
            prevention="Size connection pools based on concurrency requirements; monitor pool utilization; "
            "use separate pools per service boundary",
            category="infrastructure",
            severity="high",
        )
        m8 = mgr.log_mistake(
            error_description="API versioning not implemented — breaking change in /api/users response "
            "format broke all mobile clients",
            context="Response field 'name' was renamed to 'full_name' without versioning",
            correction="Introduced URL-based versioning (/api/v1/, /api/v2/); kept v1 backward "
            "compatible; added deprecation headers",
            prevention="Always version APIs from day one; use content negotiation or URL versioning; "
            "document breaking changes in changelog",
            category="api",
            severity="high",
        )
        summary["mistakes"] = 8

        # ── Patterns (8) ─────────────────────────────────────────────
        p1 = mgr.store_pattern(
            name="CQRS (Command Query Responsibility Segregation)",
            description="Separate read and write models to optimize each independently. Commands mutate "
            "state through domain logic; queries read from denormalized read-optimized views.",
            code_example="class CreateOrderCommand:\n    def execute(self, data: OrderInput) -> str:\n"
            "        order = Order.create(data)\n        self.event_store.append(OrderCreated(order))\n"
            "        return order.id\n\nclass OrderQueryService:\n    def get_order(self, order_id: str) -> OrderView:\n"
            "        return self.read_db.find_one({'order_id': order_id})",
            language="python",
            category="architecture",
            tags=["pattern", "architecture", "cqrs"],
        )
        p2 = mgr.store_pattern(
            name="API Gateway Pattern",
            description="Single entry point that routes requests to appropriate microservices, handling "
            "cross-cutting concerns like auth, rate limiting, logging, and request transformation.",
            code_example="# Kong/Nginx/Envoy configuration concept\nroutes:\n  - path: /api/users\n"
            "    service: user-service\n    plugins: [jwt-auth, rate-limit, cors]\n"
            "  - path: /api/orders\n    service: order-service\n    plugins: [jwt-auth, rate-limit]",
            language="yaml",
            category="architecture",
            tags=["pattern", "architecture", "api-gateway"],
        )
        p3 = mgr.store_pattern(
            name="Saga Pattern for Distributed Transactions",
            description="Coordinate multi-service transactions using a sequence of local transactions "
            "with compensating actions for rollback. Prefer choreography for simple flows, "
            "orchestration for complex ones.",
            code_example="class OrderSaga:\n    steps = [\n        SagaStep(action=reserve_inventory, compensate=release_inventory),\n"
            "        SagaStep(action=process_payment, compensate=refund_payment),\n"
            "        SagaStep(action=schedule_shipment, compensate=cancel_shipment),\n    ]\n\n"
            "    async def execute(self, order: Order):\n        completed = []\n"
            "        for step in self.steps:\n            try:\n                await step.action(order)\n"
            "                completed.append(step)\n            except Exception:\n"
            "                for s in reversed(completed):\n                    await s.compensate(order)\n"
            "                raise",
            language="python",
            category="architecture",
            tags=["pattern", "architecture", "saga", "distributed"],
        )
        p4 = mgr.store_pattern(
            name="Bulkhead Isolation",
            description="Isolate critical resources (thread pools, connection pools, memory) per service "
            "or feature to prevent a failure in one area from consuming all shared resources.",
            code_example="# Separate thread pools per external dependency\npayment_pool = ThreadPoolExecutor(max_workers=10, thread_name_prefix='payment')\n"
            "inventory_pool = ThreadPoolExecutor(max_workers=10, thread_name_prefix='inventory')\n\n"
            "async def process_order(order):\n    payment = await loop.run_in_executor(payment_pool, charge, order)\n"
            "    inventory = await loop.run_in_executor(inventory_pool, reserve, order)",
            language="python",
            category="resilience",
            tags=["pattern", "resilience", "bulkhead"],
        )
        p5 = mgr.store_pattern(
            name="Database Migration with Zero Downtime",
            description="Apply schema changes without downtime using expand-contract pattern: "
            "1) Add new column (expand), 2) Backfill data, 3) Update app to use new column, "
            "4) Remove old column (contract).",
            code_example="# Step 1: Expand — add new column\nALTER TABLE users ADD COLUMN full_name VARCHAR(200);\n\n"
            "# Step 2: Backfill\nUPDATE users SET full_name = first_name || ' ' || last_name;\n\n"
            "# Step 3: App reads from full_name (deploy)\n# Step 4: Contract — drop old columns\n"
            "ALTER TABLE users DROP COLUMN first_name, DROP COLUMN last_name;",
            language="sql",
            category="devops",
            tags=["pattern", "devops", "database", "migration"],
        )
        p6 = mgr.store_pattern(
            name="Contract Testing with Pact",
            description="Consumer-driven contract tests verify API compatibility between services "
            "without requiring full integration environment. Each consumer defines expected "
            "interactions; provider verifies against all consumer contracts.",
            code_example="# Consumer test\ndef test_get_user(pact):\n    pact.given('user 123 exists').upon_receiving('a request for user 123')\n"
            "        .with_request('GET', '/api/users/123')\n"
            "        .will_respond_with(200, body={'id': '123', 'name': Like('John')})\n\n"
            "    with pact:\n        result = UserClient().get_user('123')\n"
            "        assert result.name is not None",
            language="python",
            category="testing",
            tags=["pattern", "testing", "contract", "pact"],
        )
        p7 = mgr.store_pattern(  # noqa: F841
            name="Strangler Fig Migration",
            description="Incrementally migrate a legacy system by routing new features to the new system "
            "while keeping the old system running. Gradually redirect traffic until the legacy "
            "system can be decommissioned.",
            code_example="# Nginx routing — gradually shift traffic\nupstream legacy { server legacy-app:8080; }\n"
            "upstream modern { server new-app:8080; }\n\n"
            "location /api/users { proxy_pass http://modern; }   # migrated\n"
            "location /api/orders { proxy_pass http://modern; }   # migrated\n"
            "location /api/ { proxy_pass http://legacy; }          # not yet migrated",
            language="nginx",
            category="architecture",
            tags=["pattern", "architecture", "migration", "strangler-fig"],
        )
        p8 = mgr.store_pattern(
            name="Graceful Degradation",
            description="When a non-critical dependency fails, serve a degraded but functional response "
            "instead of returning an error. Cache last-known-good responses for fallback.",
            code_example="async def get_product_with_recommendations(product_id: str):\n"
            "    product = await product_service.get(product_id)  # critical\n"
            "    try:\n        recommendations = await recommendation_service.get(product_id)\n"
            "    except ServiceUnavailable:\n"
            "        recommendations = cache.get(f'recs:{product_id}', default=[])\n"
            "    return {**product, 'recommendations': recommendations}",
            language="python",
            category="resilience",
            tags=["pattern", "resilience", "graceful-degradation"],
        )
        summary["patterns"] = 8

        # ── Decisions (5) ─────────────────────────────────────────────
        d1 = mgr.store_decision(
            title="GraphQL Federation over REST aggregation layer",
            description="Adopt Apollo Federation as the API gateway pattern instead of building a "
            "custom REST aggregation service.",
            rationale="Federation lets each team own their subgraph independently while providing a "
            "unified schema for clients. Eliminates over-fetching and under-fetching. "
            "TypeScript type generation gives frontend teams compile-time safety.",
            alternatives=[
                "Custom REST aggregation",
                "gRPC with REST gateway",
                "Single monolith API",
            ],
            chosen="Apollo Federation v2 with managed schema registry",
            tags=["decision", "api", "graphql"],
        )
        d2 = mgr.store_decision(
            title="Redis Sentinel over Redis Cluster for caching",
            description="Use Redis Sentinel for high availability instead of Redis Cluster after "
            "cluster deployment failed during partition testing.",
            rationale="Our dataset is under 50GB — Cluster's sharding adds complexity we don't need. "
            "Sentinel provides automatic failover with simpler operations. Can migrate to "
            "Cluster later if data exceeds single-node capacity.",
            alternatives=["Redis Cluster", "AWS ElastiCache", "Memcached", "KeyDB"],
            chosen="Redis 7.x with 3-node Sentinel quorum",
            tags=["decision", "infrastructure", "redis"],
        )
        d3 = mgr.store_decision(
            title="OpenTelemetry for unified observability",
            description="Standardize on OpenTelemetry SDK for all telemetry (traces, metrics, logs) "
            "across microservices.",
            rationale="Vendor-neutral standard avoids lock-in. Single SDK replaces separate "
            "Prometheus client, Jaeger client, and custom logging libraries. OTLP protocol "
            "supported by all major backends (Jaeger, Grafana, Datadog).",
            alternatives=["Datadog APM", "New Relic", "Jaeger + Prometheus (separate SDKs)"],
            chosen="OpenTelemetry SDK with OTLP Collector exporting to Jaeger + Prometheus",
            tags=["decision", "observability", "opentelemetry"],
        )
        d4 = mgr.store_decision(
            title="Playwright over Cypress for E2E testing",
            description="Standardize on Playwright for end-to-end browser testing across the organization.",
            rationale="Playwright supports all browsers (Chromium, Firefox, WebKit) with a single API. "
            "Built-in auto-waiting eliminates flaky selectors. Parallel execution and "
            "sharding reduce CI time by 60% compared to Cypress.",
            alternatives=["Cypress", "Selenium", "TestCafe", "Puppeteer"],
            chosen="Playwright with TypeScript, sharded across 4 CI workers",
            tags=["decision", "testing", "e2e"],
        )
        d5 = mgr.store_decision(
            title="SSE over WebSocket for real-time notifications",
            description="Use Server-Sent Events instead of WebSocket for the notification system "
            "after WebSocket scaling issues.",
            rationale="SSE is HTTP-native (works through proxies/CDNs), auto-reconnects, and doesn't "
            "require sticky sessions. Our notifications are server→client only, making SSE "
            "a perfect fit. Combined with Redis pub/sub for horizontal scaling.",
            alternatives=[
                "WebSocket (Socket.IO)",
                "Long polling",
                "gRPC streaming",
                "Firebase Cloud Messaging",
            ],
            chosen="SSE with Redis pub/sub fanout for stateless scaling",
            tags=["decision", "architecture", "realtime"],
        )
        summary["decisions"] = 5

        # ── Conversations (4) ─────────────────────────────────────────
        c1 = mgr.store_conversation(
            messages=[
                {
                    "role": "user",
                    "content": "Our GraphQL API is getting hammered by deeply nested queries. Someone sent a query with 15 levels of nesting and it pegged the CPU at 100% for 30 seconds.",
                },
                {
                    "role": "claude",
                    "content": "This is a classic GraphQL complexity attack. I recommend a three-layer defense:\n1. Query depth limiting (max 7-10 levels)\n2. Query complexity analysis (assign cost per field, reject queries over threshold)\n3. Persisted queries in production (only allow pre-registered query hashes)",
                },
                {"role": "user", "content": "Can we implement all three right now?"},
                {
                    "role": "claude",
                    "content": "Done. I've added:\n- graphql-depth-limit middleware (max=7)\n- graphql-query-complexity with field-level cost annotations (max=1000)\n- Automatic Persisted Queries via Apollo Server's APQ plugin\nAlso added a query execution time metric to Prometheus for monitoring.",
                },
            ],
            summary="Mitigating GraphQL complexity attacks with depth limits, cost analysis, and persisted queries",
            session_id="session-team-001",
            participants=["user", "claude"],
            tags=["security", "graphql", "performance"],
        )
        c2 = mgr.store_conversation(
            messages=[
                {
                    "role": "user",
                    "content": "The Terraform apply just deleted our production database. We need to restore from backup immediately.",
                },
                {
                    "role": "gemini",
                    "content": "I see the issue — the RDS instance was recreated because the engine_version parameter changed, and there's no lifecycle prevent_destroy rule. Let me initiate restore from the latest automated snapshot (3 hours old). Manual snapshot from last night is also available.",
                },
                {
                    "role": "user",
                    "content": "Use the manual snapshot from last night — it's before the bad data migration ran.",
                },
                {
                    "role": "gemini",
                    "content": "Restoring from snapshot 'manual-2024-01-14-pre-migration'. ETA: 25-35 minutes for a db.r6g.xlarge. I'm also adding prevent_destroy to all stateful Terraform resources and setting up a pre-apply CI check that flags any resource destruction.",
                },
                {
                    "role": "user",
                    "content": "Database is back. What do we need to do to prevent this from happening again?",
                },
                {
                    "role": "gemini",
                    "content": "Prevention plan:\n1. ✅ Added lifecycle { prevent_destroy = true } to RDS, S3, ElastiCache\n2. ✅ CI pipeline now runs terraform plan and blocks if any destroy actions detected\n3. 📋 TODO: Separate stateful resources into their own Terraform state file\n4. 📋 TODO: Set up automated WAL-G continuous archiving for point-in-time recovery\n5. 📋 TODO: Quarterly disaster recovery drills",
                },
            ],
            summary="Incident response: Terraform destroyed production RDS; restored from snapshot; prevention plan created",
            session_id="session-team-002",
            participants=["user", "gemini"],
            tags=["incident", "terraform", "disaster-recovery"],
        )
        c3 = mgr.store_conversation(
            messages=[
                {
                    "role": "user",
                    "content": "We need to choose between Cypress and Playwright for our E2E test suite. What are the trade-offs?",
                },
                {
                    "role": "claude",
                    "content": "Key comparison:\n\n**Playwright pros:** Multi-browser (Chromium, FF, WebKit), faster execution, built-in auto-wait, native parallel/sharding, better debugging (trace viewer)\n\n**Cypress pros:** Better DX for simple tests, time-travel debugging, larger ecosystem of plugins, component testing built-in\n\n**Playwright cons:** Steeper learning curve, smaller plugin ecosystem\n**Cypress cons:** Chromium-only for free tier, no native sharding, struggles with multi-tab/multi-origin",
                },
                {
                    "role": "user",
                    "content": "We need cross-browser testing and fast CI. Sounds like Playwright wins for us.",
                },
                {
                    "role": "claude",
                    "content": "Agreed. I'll set up Playwright with:\n- TypeScript config for type safety\n- 4-worker sharding in GitHub Actions\n- HTML reporter with trace artifacts on failure\n- Page Object Model structure for maintainability\n- Visual comparison testing for UI regression",
                },
            ],
            summary="E2E framework comparison: chose Playwright over Cypress for cross-browser support and CI performance",
            session_id="session-team-003",
            participants=["user", "claude"],
            tags=["testing", "e2e", "tooling-decision"],
        )
        c4 = mgr.store_conversation(
            messages=[
                {
                    "role": "user",
                    "content": "Our microservices are all logging differently — some use print(), some use logging module, some use structlog. It's impossible to correlate requests across services.",
                },
                {
                    "role": "copilot",
                    "content": "Let's standardize on structured JSON logging with correlation. I propose:\n1. structlog for all Python services\n2. Every log line includes: timestamp, level, service_name, trace_id, span_id\n3. Logs shipped to Loki via Promtail\n4. Grafana for querying with trace_id correlation",
                },
                {
                    "role": "user",
                    "content": "How do we propagate the trace_id across service boundaries?",
                },
                {
                    "role": "copilot",
                    "content": "OpenTelemetry handles this automatically. The OTel SDK:\n1. Generates trace_id on the first service (API gateway)\n2. Propagates via W3C Trace Context headers (traceparent)\n3. Each service's structlog processor extracts trace_id from the current span\n\nI'll set up a shared logging configuration package that all services import.",
                },
            ],
            summary="Standardizing structured logging across microservices with structlog, OpenTelemetry trace correlation, and Loki",
            session_id="session-team-004",
            participants=["user", "copilot"],
            tags=["observability", "logging", "standardization"],
        )
        summary["conversations"] = 4

        # ── Edges (28) ────────────────────────────────────────────────
        edges = [
            # Mistake → Task (CAUSED_BY)
            (
                m1,
                t2,
                EdgeType.CAUSED_BY,
                1.0,
                {"context": "GraphQL depth exploit discovered on federation gateway"},
            ),
            (
                m2,
                t10,
                EdgeType.CAUSED_BY,
                1.0,
                {"context": "Terraform destroyed RDS due to missing lifecycle rule"},
            ),
            (
                m4,
                t8,
                EdgeType.CAUSED_BY,
                0.9,
                {"context": "WebSocket leak discovered during notification system build"},
            ),
            (
                m5,
                t1,
                EdgeType.CAUSED_BY,
                0.8,
                {"context": "JWT expiry issue found during auth implementation review"},
            ),
            # Pattern → Mistake (FIXED_BY)
            (
                p4,
                m7,
                EdgeType.FIXED_BY,
                1.0,
                {"context": "Bulkhead isolation fixes connection pool exhaustion"},
            ),
            (
                p8,
                m4,
                EdgeType.FIXED_BY,
                0.9,
                {"context": "Graceful degradation prevents cascading failures from leaks"},
            ),
            (
                p2,
                m8,
                EdgeType.FIXED_BY,
                0.8,
                {"context": "API gateway pattern enforces versioning at the boundary"},
            ),
            # Task → Task (PRECEDED_BY)
            (
                t6,
                t4,
                EdgeType.PRECEDED_BY,
                0.7,
                {"context": "Tracing instrumented before E2E tests to aid debugging"},
            ),
            (
                t1,
                t9,
                EdgeType.PRECEDED_BY,
                0.9,
                {"context": "Auth implementation preceded rate limiting design"},
            ),
            (
                t5,
                t9,
                EdgeType.PRECEDED_BY,
                0.6,
                {"context": "Redis setup preceded rate limiter using Redis sorted sets"},
            ),
            # Decision → Task (USED_IN)
            (
                d1,
                t2,
                EdgeType.USED_IN,
                1.0,
                {"context": "GraphQL federation decision drove gateway implementation"},
            ),
            (
                d2,
                t5,
                EdgeType.USED_IN,
                0.9,
                {"context": "Redis Sentinel decision followed cluster failure"},
            ),
            (
                d3,
                t6,
                EdgeType.USED_IN,
                1.0,
                {"context": "OpenTelemetry decision drove tracing integration"},
            ),
            (
                d4,
                t4,
                EdgeType.USED_IN,
                1.0,
                {"context": "Playwright decision drove E2E test suite creation"},
            ),
            (
                d5,
                t8,
                EdgeType.USED_IN,
                0.9,
                {"context": "SSE decision replaced failed WebSocket approach"},
            ),
            # Pattern → Decision (REFERENCES)
            (
                p2,
                d1,
                EdgeType.REFERENCES,
                0.9,
                {"context": "API gateway pattern referenced in federation decision"},
            ),
            (
                p3,
                d5,
                EdgeType.REFERENCES,
                0.7,
                {"context": "Saga pattern informed SSE architecture decision"},
            ),
            (
                p6,
                d4,
                EdgeType.REFERENCES,
                0.8,
                {"context": "Contract testing pattern influenced E2E testing decision"},
            ),
            # Similar patterns
            (
                p4,
                p8,
                EdgeType.SIMILAR_TO,
                0.8,
                {"context": "Both are resilience patterns for failure isolation"},
            ),
            (
                p1,
                p3,
                EdgeType.SIMILAR_TO,
                0.7,
                {"context": "Both handle distributed data consistency"},
            ),
            # Conversations → Tasks (RELATED_TO)
            (
                c1,
                t2,
                EdgeType.RELATED_TO,
                1.0,
                {"context": "GraphQL attack discussion tied to gateway task"},
            ),
            (c2, t10, EdgeType.RELATED_TO, 1.0, {"context": "Terraform incident tied to IaC task"}),
            (
                c3,
                t4,
                EdgeType.RELATED_TO,
                1.0,
                {"context": "E2E framework comparison tied to Playwright task"},
            ),
            (
                c4,
                t6,
                EdgeType.RELATED_TO,
                0.9,
                {"context": "Logging standardization tied to OTel tracing task"},
            ),
            # LEARNED_FROM — mistakes that led to patterns/decisions
            (
                d2,
                m7,
                EdgeType.LEARNED_FROM,
                0.9,
                {"context": "Redis Sentinel decision learned from pool exhaustion"},
            ),
            (
                d5,
                m4,
                EdgeType.LEARNED_FROM,
                0.8,
                {"context": "SSE decision learned from WebSocket connection leak"},
            ),
            (
                p5,
                m2,
                EdgeType.LEARNED_FROM,
                0.9,
                {"context": "Zero-downtime migration pattern learned from Terraform incident"},
            ),
            # Task → Pattern (USED_IN)
            (
                p1,
                t2,
                EdgeType.USED_IN,
                0.9,
                {"context": "CQRS pattern applied in GraphQL query service"},
            ),
        ]

        for src, tgt, etype, weight, meta in edges:
            mgr.link_nodes(
                source_id=src,
                target_id=tgt,
                edge_type=etype,
                weight=weight,
                metadata=meta,
            )
        summary["edges"] = len(edges)

    finally:
        mgr.close()

    return summary


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def _print_summary(name: str, summary: dict[str, int]) -> None:
    """Pretty-print the seeding summary for one system."""
    if not summary:
        return
    total = sum(summary.values())
    if total == 0:
        return
    print(f"\n  📊  {name} summary:")
    for kind, count in summary.items():
        print(f"       {kind:>15s}: {count}")
    print(f"       {'total':>15s}: {total}")


def main() -> None:
    """CLI entrypoint for seeding context graphs."""
    parser = argparse.ArgumentParser(
        description="Seed context graphs with realistic development data.",
    )
    parser.add_argument(
        "--system",
        choices=["orchestrator", "agentic_team"],
        default=None,
        help="Seed only the specified system (default: both)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-seed even if data already exists",
    )
    args = parser.parse_args()

    print("🌱  Context Graph Seeder")
    print("=" * 40)

    if args.system in (None, "orchestrator"):
        print("\n▶  Seeding orchestrator context graph …")
        orch_summary = seed_orchestrator(force=args.force)
        _print_summary("Orchestrator", orch_summary)

    if args.system in (None, "agentic_team"):
        print("\n▶  Seeding agentic team context graph …")
        team_summary = seed_agentic_team(force=args.force)
        _print_summary("Agentic Team", team_summary)

    print("\n✅  Done.")


if __name__ == "__main__":
    main()
