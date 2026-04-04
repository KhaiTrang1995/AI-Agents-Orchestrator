"""Context Export/Import - Backup, migration, and analysis support."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.etree.ElementTree import Element, ElementTree, SubElement

from orchestrator.context.models.schemas import Edge, Node
from orchestrator.context.store.graph_store import GraphStore


class ContextExporter:
    """Export and import context graph data for backup, migration, and analysis."""

    EXPORT_VERSION = "1.0"

    def __init__(self, graph_store: GraphStore):
        """Initialize exporter.

        Args:
            graph_store: Graph store instance
        """
        self.logger = logging.getLogger("context.export")
        self.graph_store = graph_store

    def export_json(
        self,
        output_path: str,
        node_types: list[str] | None = None,
    ) -> dict[str, Any]:
        """Export nodes and edges to a JSON file.

        Args:
            output_path: Path for the output JSON file
            node_types: Optional list of node types to filter export

        Returns:
            Stats about what was exported
        """
        nodes_data: list[dict[str, Any]] = []
        edges_data: list[dict[str, Any]] = []

        with self.graph_store._transaction() as cursor:
            if node_types:
                placeholders = ",".join("?" * len(node_types))
                cursor.execute(
                    f"SELECT * FROM nodes WHERE node_type IN ({placeholders})",  # noqa: B608
                    node_types,
                )
            else:
                cursor.execute("SELECT * FROM nodes")

            for row in cursor.fetchall():
                node = self.graph_store._row_to_node(row)
                nodes_data.append(node.to_dict())

            node_ids = {n["id"] for n in nodes_data}

            cursor.execute("SELECT * FROM edges")
            for row in cursor.fetchall():
                edge = self.graph_store._row_to_edge(row)
                if edge.source_id in node_ids and edge.target_id in node_ids:
                    edges_data.append(edge.to_dict())

        export_data = {
            "version": self.EXPORT_VERSION,
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "stats": {"nodes": len(nodes_data), "edges": len(edges_data)},
            "nodes": nodes_data,
            "edges": edges_data,
        }

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, default=str)

        self.logger.info(
            f"Exported {len(nodes_data)} nodes and {len(edges_data)} edges to {output_path}"
        )

        return {
            "output_path": output_path,
            "nodes_exported": len(nodes_data),
            "edges_exported": len(edges_data),
            "node_types_filter": node_types,
        }

    def import_json(
        self,
        input_path: str,
        merge: bool = True,
    ) -> dict[str, Any]:
        """Import nodes and edges from a JSON file.

        Args:
            input_path: Path to the JSON file to import
            merge: If True, skip existing node IDs; if False, replace them

        Returns:
            Stats about the import
        """
        with open(input_path, encoding="utf-8") as f:
            data = json.load(f)

        nodes_imported = 0
        nodes_skipped = 0
        edges_imported = 0
        edges_skipped = 0

        for node_data in data.get("nodes", []):
            node = Node.from_dict(node_data)
            existing = self.graph_store.get_node(node.id)

            if existing and merge:
                nodes_skipped += 1
                continue

            self.graph_store.add_node(node)
            nodes_imported += 1

        for edge_data in data.get("edges", []):
            edge = Edge.from_dict(edge_data)
            existing = self.graph_store.get_edge(edge.id)

            if existing and merge:
                edges_skipped += 1
                continue

            try:
                self.graph_store.add_edge(edge)
                edges_imported += 1
            except Exception as e:
                self.logger.warning(f"Failed to import edge {edge.id}: {e}")
                edges_skipped += 1

        self.logger.info(
            f"Imported {nodes_imported} nodes and {edges_imported} edges from {input_path}"
        )

        return {
            "input_path": input_path,
            "merge_mode": merge,
            "nodes_imported": nodes_imported,
            "nodes_skipped": nodes_skipped,
            "edges_imported": edges_imported,
            "edges_skipped": edges_skipped,
        }

    def export_graphml(self, output_path: str) -> dict[str, Any]:
        """Export to GraphML XML format for visualization tools like Gephi.

        Args:
            output_path: Path for the output GraphML file

        Returns:
            Stats about what was exported
        """
        graphml = Element("graphml")
        graphml.set("xmlns", "http://graphml.graphstruct.org/xmlns")

        # Define attribute keys for nodes
        for attr_name, attr_type in [
            ("node_type", "string"),
            ("title", "string"),
            ("content", "string"),
            ("importance_score", "double"),
            ("created_at", "string"),
        ]:
            key_el = SubElement(graphml, "key")
            key_el.set("id", attr_name)
            key_el.set("for", "node")
            key_el.set("attr.name", attr_name)
            key_el.set("attr.type", attr_type)

        # Define attribute keys for edges
        for attr_name, attr_type in [
            ("edge_type", "string"),
            ("weight", "double"),
        ]:
            key_el = SubElement(graphml, "key")
            key_el.set("id", attr_name)
            key_el.set("for", "edge")
            key_el.set("attr.name", attr_name)
            key_el.set("attr.type", attr_type)

        graph = SubElement(graphml, "graph")
        graph.set("id", "context_graph")
        graph.set("edgedefault", "directed")

        node_count = 0
        edge_count = 0

        with self.graph_store._transaction() as cursor:
            cursor.execute("SELECT * FROM nodes")
            for row in cursor.fetchall():
                node = self.graph_store._row_to_node(row)
                node_el = SubElement(graph, "node")
                node_el.set("id", node.id)

                for key, value in [
                    ("node_type", node.node_type.value),
                    ("title", node.title),
                    ("content", node.content[:500]),
                    ("importance_score", str(node.importance_score)),
                    ("created_at", node.created_at.isoformat()),
                ]:
                    data_el = SubElement(node_el, "data")
                    data_el.set("key", key)
                    data_el.text = value

                node_count += 1

            cursor.execute("SELECT * FROM edges")
            for row in cursor.fetchall():
                edge = self.graph_store._row_to_edge(row)
                edge_el = SubElement(graph, "edge")
                edge_el.set("id", edge.id)
                edge_el.set("source", edge.source_id)
                edge_el.set("target", edge.target_id)

                for key, value in [
                    ("edge_type", edge.edge_type.value),
                    ("weight", str(edge.weight)),
                ]:
                    data_el = SubElement(edge_el, "data")
                    data_el.set("key", key)
                    data_el.text = value

                edge_count += 1

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        tree = ElementTree(graphml)
        tree.write(output_path, encoding="unicode", xml_declaration=True)

        self.logger.info(
            f"Exported {node_count} nodes and {edge_count} edges to GraphML at {output_path}"
        )

        return {
            "output_path": output_path,
            "format": "graphml",
            "nodes_exported": node_count,
            "edges_exported": edge_count,
        }

    def get_export_summary(self) -> dict[str, Any]:
        """Get a summary of what would be exported without writing files.

        Returns:
            Summary with counts by type
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
