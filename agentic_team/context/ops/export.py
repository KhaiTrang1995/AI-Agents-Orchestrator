"""
Context Export/Import — Backup and migration for Agentic Team Context.

Independent implementation — does NOT import from orchestrator/context.
Supports JSON export/import for backup, migration, and analysis.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agentic_team.context.models.schemas import Edge, Node
from agentic_team.context.store.graph_store import GraphStore


class ContextExporter:
    """Export and import agentic team context graph data."""

    EXPORT_VERSION = "1.0"

    def __init__(self, graph_store: GraphStore):
        """Initialize exporter.

        Args:
            graph_store: Graph store instance.
        """
        self.logger = logging.getLogger("agentic_team.context.export")
        self.graph_store = graph_store

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_json(
        self,
        output_path: str,
        node_types: list[str] | None = None,
    ) -> dict[str, Any]:
        """Export nodes and edges to a JSON file.

        Args:
            output_path: Destination file path.
            node_types: Optional filter — export only these node types.

        Returns:
            Statistics dict.
        """
        nodes_data: list[dict[str, Any]] = []
        edges_data: list[dict[str, Any]] = []

        with self.graph_store._transaction() as cursor:
            if node_types:
                placeholders = ",".join("?" * len(node_types))
                cursor.execute(
                    f"SELECT * FROM nodes WHERE node_type IN ({placeholders})",  # noqa: S608
                    node_types,
                )
            else:
                cursor.execute("SELECT * FROM nodes")

            for row in cursor.fetchall():
                node = self.graph_store._row_to_node(row)
                nodes_data.append(node.to_dict())

            exported_ids = {n["id"] for n in nodes_data}

            cursor.execute("SELECT * FROM edges")
            for row in cursor.fetchall():
                edge = self.graph_store._row_to_edge(row)
                if edge.source_id in exported_ids and edge.target_id in exported_ids:
                    edges_data.append(edge.to_dict())

        payload = {
            "version": self.EXPORT_VERSION,
            "system": "agentic_team",
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "stats": {"nodes": len(nodes_data), "edges": len(edges_data)},
            "nodes": nodes_data,
            "edges": edges_data,
        }

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, default=str)

        self.logger.info(
            "Exported %d nodes and %d edges to %s",
            len(nodes_data),
            len(edges_data),
            output_path,
        )

        return {
            "output_path": output_path,
            "nodes_exported": len(nodes_data),
            "edges_exported": len(edges_data),
            "node_types_filter": node_types,
        }

    # ------------------------------------------------------------------
    # Import
    # ------------------------------------------------------------------

    def import_json(
        self,
        input_path: str,
        merge: bool = True,
    ) -> dict[str, Any]:
        """Import nodes and edges from a JSON file.

        Args:
            input_path: Source file path.
            merge: If True, skip existing node IDs; if False, overwrite.

        Returns:
            Statistics dict.
        """
        with open(input_path, encoding="utf-8") as fh:
            data = json.load(fh)

        nodes_imported = 0
        nodes_skipped = 0
        edges_imported = 0
        edges_skipped = 0

        for node_data in data.get("nodes", []):
            node = Node.from_dict(node_data)
            if merge and self.graph_store.get_node(node.id):
                nodes_skipped += 1
                continue
            self.graph_store.add_node(node)
            nodes_imported += 1

        for edge_data in data.get("edges", []):
            edge = Edge.from_dict(edge_data)
            if merge and self.graph_store.get_edge(edge.id):
                edges_skipped += 1
                continue
            try:
                self.graph_store.add_edge(edge)
                edges_imported += 1
            except Exception as exc:
                self.logger.warning("Failed to import edge %s: %s", edge.id, exc)
                edges_skipped += 1

        self.logger.info(
            "Imported %d nodes and %d edges from %s",
            nodes_imported,
            edges_imported,
            input_path,
        )

        return {
            "input_path": input_path,
            "merge_mode": merge,
            "nodes_imported": nodes_imported,
            "nodes_skipped": nodes_skipped,
            "edges_imported": edges_imported,
            "edges_skipped": edges_skipped,
        }

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def get_export_summary(self) -> dict[str, Any]:
        """Preview what would be exported without writing files.

        Returns:
            Summary dict with counts by type.
        """
        with self.graph_store._transaction() as cursor:
            cursor.execute("SELECT node_type, COUNT(*) FROM nodes GROUP BY node_type")
            node_counts = {row[0]: row[1] for row in cursor.fetchall()}

            cursor.execute("SELECT edge_type, COUNT(*) FROM edges GROUP BY edge_type")
            edge_counts = {row[0]: row[1] for row in cursor.fetchall()}

            cursor.execute("SELECT COUNT(*) FROM nodes")
            total_nodes = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM edges")
            total_edges = cursor.fetchone()[0]

        return {
            "total_nodes": total_nodes,
            "total_edges": total_edges,
            "nodes_by_type": node_counts,
            "edges_by_type": edge_counts,
        }
