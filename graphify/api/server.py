"""
Graphify REST API — production-ready Flask server for querying project graphs.

Features:
  - CORS support for cross-origin frontend access
  - Global error handling with structured JSON responses
  - Request parameter validation
  - Metrics endpoint for scan history
  - Diff/snapshot management endpoints

Start with: ``python -m graphify serve --db /path/to/.graphify.db``
"""

from __future__ import annotations

import logging

from graphify.core.differ import GraphDiffer
from graphify.core.exceptions import GraphifyError, ValidationError
from graphify.core.graph import GraphStore
from graphify.core.metrics import MetricsStore
from graphify.export.formatters import GraphExporter
from graphify.search.fts_engine import FTSEngine
from graphify.search.query_engine import QueryEngine

logger = logging.getLogger(__name__)

_store: GraphStore | None = None
_fts: FTSEngine | None = None
_query: QueryEngine | None = None
_exporter: GraphExporter | None = None
_metrics: MetricsStore | None = None
_differ: GraphDiffer | None = None


def _safe_int(value: str | None, default: int, lo: int = 1, hi: int = 500) -> int:
    """Parse an integer query param within bounds."""
    if value is None:
        return default
    try:
        n = int(value)
    except (ValueError, TypeError):
        return default
    return max(lo, min(n, hi))


def create_app(db_path: str = ":memory:") -> Flask:  # type: ignore[name-defined]  # noqa: C901,F821  # pylint: disable=undefined-variable
    """Create and configure the Flask application."""
    from flask import Flask, jsonify, request  # pylint: disable=C0415

    global _store, _fts, _query, _exporter, _metrics, _differ  # noqa: PLW0603

    app = Flask(__name__)
    _store = GraphStore(db_path)
    _fts = FTSEngine(_store)
    _query = QueryEngine(_store)
    _exporter = GraphExporter(_store)
    _metrics = MetricsStore(_store._get_conn)  # noqa: SLF001
    _differ = GraphDiffer(_store._get_conn)  # noqa: SLF001

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------

    @app.after_request
    def _add_cors(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    # ------------------------------------------------------------------
    # Global error handling
    # ------------------------------------------------------------------

    @app.errorhandler(ValidationError)
    def _handle_validation(exc):
        return jsonify({"error": str(exc), "code": exc.code, "field": exc.field}), 400

    @app.errorhandler(GraphifyError)
    def _handle_graphify(exc):
        return jsonify({"error": str(exc), "code": exc.code}), 500

    @app.errorhandler(404)
    def _handle_404(_exc):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(Exception)
    def _handle_generic(exc):
        logger.exception("Unhandled error: %s", exc)
        return jsonify({"error": "Internal server error", "detail": str(exc)}), 500

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    @app.route("/api/health")
    def health():
        stats = _store.stats("")
        return jsonify({"status": "ok", "db": db_path, "total_nodes": stats.get("nodes", 0)})

    # ------------------------------------------------------------------
    # Projects
    # ------------------------------------------------------------------

    @app.route("/api/projects")
    def list_projects():
        projects = _store.list_projects()
        return jsonify(
            [
                {
                    "project_id": p.project_id,
                    "name": p.name,
                    "root_path": p.root_path,
                    "total_files": p.total_files,
                    "total_lines": p.total_lines,
                    "languages": p.languages,
                    "scanned_at": p.scanned_at,
                }
                for p in projects
            ]
        )

    @app.route("/api/projects/<project_id>")
    def get_project(project_id):
        return jsonify(_query.summary(project_id))

    @app.route("/api/projects/<project_id>/stats")
    def project_stats(project_id):
        return jsonify(_store.stats(project_id))

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    @app.route("/api/search")
    def search():
        q = request.args.get("q", "").strip()
        project_id = request.args.get("project_id", "")
        limit = _safe_int(request.args.get("limit"), 50, hi=500)
        if not q:
            return jsonify({"error": "Missing 'q' parameter"}), 400
        results = _fts.search(q, project_id=project_id, limit=limit)
        return jsonify(
            [
                {
                    "name": r["node"].name,
                    "type": r["node"].node_type.value,
                    "file": r["node"].file_path,
                    "score": r["score"],
                    "snippet": r["snippet"],
                }
                for r in results
            ]
        )

    @app.route("/api/search/name")
    def search_name():
        name = request.args.get("name", "").strip()
        project_id = request.args.get("project_id", "")
        if not name:
            return jsonify({"error": "Missing 'name' parameter"}), 400
        nodes = _fts.search_by_name(name, project_id=project_id)
        return jsonify(
            [
                {"id": n.id, "name": n.name, "type": n.node_type.value, "file": n.file_path}
                for n in nodes
            ]
        )

    # ------------------------------------------------------------------
    # Graph queries
    # ------------------------------------------------------------------

    @app.route("/api/files/<path:file_path>")
    def file_structure(file_path):
        project_id = request.args.get("project_id", "")
        return jsonify(_query.get_file_structure(file_path, project_id))

    @app.route("/api/classes")
    def class_hierarchy():
        project_id = request.args.get("project_id", "")
        return jsonify(_query.get_class_hierarchy(project_id))

    @app.route("/api/dependencies")
    def dependencies():
        project_id = request.args.get("project_id", "")
        return jsonify(_query.get_dependencies(project_id))

    @app.route("/api/tests")
    def tests():
        project_id = request.args.get("project_id", "")
        return jsonify(_query.get_tests(project_id))

    @app.route("/api/hotspots")
    def hotspots():
        project_id = request.args.get("project_id", "")
        top_n = _safe_int(request.args.get("top"), 20, hi=100)
        return jsonify(_query.complexity_hotspots(project_id, top_n))

    @app.route("/api/languages")
    def languages():
        project_id = request.args.get("project_id", "")
        return jsonify(_query.language_breakdown(project_id))

    @app.route("/api/subgraph/<node_id>")
    def subgraph(node_id):
        depth = _safe_int(request.args.get("depth"), 3, hi=5)
        return jsonify(_query.get_subgraph(node_id, max_depth=depth))

    # ------------------------------------------------------------------
    # Intelligence
    # ------------------------------------------------------------------

    @app.route("/api/god-nodes")
    def api_god_nodes():
        project_id = request.args.get("project_id", "")
        top_n = _safe_int(request.args.get("top"), 20, hi=100)
        gods = _store.god_nodes(project_id, top_n=top_n)
        return jsonify(
            [
                {
                    "name": g["node"].name,
                    "type": g["node"].node_type.value,
                    "file": g["node"].file_path,
                    "degree": g["degree"],
                }
                for g in gods
            ]
        )

    @app.route("/api/explain/<name>")
    def api_explain(name):
        project_id = request.args.get("project_id", "")
        return jsonify(_query.explain_node(name, project_id=project_id))

    @app.route("/api/path/<start>/<end>")
    def api_path(start, end):
        project_id = request.args.get("project_id", "")
        return jsonify(_query.find_path(start, end, project_id=project_id))

    @app.route("/api/communities")
    def api_communities():
        project_id = request.args.get("project_id", "")
        communities = _query.detect_communities(project_id=project_id)
        return jsonify(
            {
                "count": len(communities),
                "communities": {
                    k: {"size": len(v), "nodes": v[:20]}
                    for k, v in sorted(
                        communities.items(),
                        key=lambda x: len(x[1]),
                        reverse=True,
                    )[:50]
                },
            }
        )

    # ------------------------------------------------------------------
    # Metrics & history
    # ------------------------------------------------------------------

    @app.route("/api/metrics/<project_id>")
    def api_metrics(project_id):
        limit = _safe_int(request.args.get("limit"), 20, hi=100)
        return jsonify(
            {
                "history": _metrics.history(project_id, limit=limit),
                "averages": _metrics.averages(project_id),
            }
        )

    # ------------------------------------------------------------------
    # Snapshots & diffing
    # ------------------------------------------------------------------

    @app.route("/api/snapshots/<project_id>")
    def api_snapshots(project_id):
        return jsonify(_differ.list_snapshots(project_id))

    @app.route("/api/snapshots/<project_id>/take", methods=["POST"])
    def api_take_snapshot(project_id):
        label = request.args.get("label", "")
        snap_id = _differ.take_snapshot(project_id, label=label)
        return jsonify({"snapshot_id": snap_id})

    @app.route("/api/diff/<int:snap_a>/<int:snap_b>")
    def api_diff(snap_a, snap_b):
        diff = _differ.diff_snapshots(snap_a, snap_b)
        return jsonify(diff.to_dict())

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    @app.route("/api/export/json")
    def export_json():
        project_id = request.args.get("project_id", "")
        return app.response_class(_exporter.to_json(project_id), mimetype="application/json")

    @app.route("/api/export/dot")
    def export_dot():
        project_id = request.args.get("project_id", "")
        return app.response_class(_exporter.to_dot(project_id), mimetype="text/plain")

    @app.route("/api/export/markdown")
    def export_markdown():
        project_id = request.args.get("project_id", "")
        return app.response_class(_exporter.to_markdown(project_id), mimetype="text/markdown")

    @app.route("/api/export/graphml")
    def export_graphml():
        project_id = request.args.get("project_id", "")
        return app.response_class(_exporter.to_graphml(project_id), mimetype="application/xml")

    return app


def run_server(db_path: str, host: str = "127.0.0.1", port: int = 5004) -> None:
    """Start the API server."""
    app = create_app(db_path)
    logger.info("Graphify API server starting on %s:%d", host, port)
    app.run(host=host, port=port)
