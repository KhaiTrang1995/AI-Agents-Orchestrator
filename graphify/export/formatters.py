"""
Export formatters — serialize the project graph to JSON, DOT (Graphviz),

GraphML, and Markdown for documentation or visualization.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from graphify.core.graph import GraphStore
from graphify.core.schema import NodeType

logger = logging.getLogger(__name__)


class GraphExporter:
    """Export a project graph to various formats."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    # ------------------------------------------------------------------
    # JSON
    # ------------------------------------------------------------------

    def to_json(self, project_id: str = "", indent: int = 2) -> str:
        """Export full graph as JSON."""
        data = self._collect(project_id)
        return json.dumps(data, indent=indent, default=str)

    # ------------------------------------------------------------------
    # DOT (Graphviz)
    # ------------------------------------------------------------------

    def to_dot(self, project_id: str = "", max_nodes: int = 500) -> str:
        """Export graph as Graphviz DOT format."""
        nodes = self._store.get_nodes(project_id=project_id, limit=max_nodes)
        edges = self._store.get_edges(project_id=project_id)

        node_ids = {n.id for n in nodes}
        lines = ["digraph project {", "  rankdir=LR;", "  node [shape=box, fontsize=10];", ""]

        # Color map by type
        colors = {
            NodeType.PROJECT: "#4CAF50",
            NodeType.DIRECTORY: "#FFC107",
            NodeType.FILE: "#2196F3",
            NodeType.CLASS: "#9C27B0",
            NodeType.FUNCTION: "#FF5722",
            NodeType.TEST: "#00BCD4",
            NodeType.IMPORT: "#607D8B",
            NodeType.DEPENDENCY: "#E91E63",
            NodeType.CONFIG: "#795548",
            NodeType.DOCUMENTATION: "#8BC34A",
        }

        for node in nodes:
            color = colors.get(node.node_type, "#9E9E9E")
            label = node.name.replace('"', '\\"')[:40]
            ntype = node.node_type.value
            lines.append(
                f'  "{node.id}" [label="{label}\\n({ntype})" '
                f'style=filled fillcolor="{color}" fontcolor=white];'
            )

        lines.append("")
        for edge in edges:
            if edge.source_id in node_ids and edge.target_id in node_ids:
                label = edge.edge_type.value
                lines.append(
                    f'  "{edge.source_id}" -> "{edge.target_id}" [label="{label}" fontsize=8];'
                )

        lines.append("}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Markdown
    # ------------------------------------------------------------------

    def to_markdown(self, project_id: str = "") -> str:
        """Export project summary as Markdown."""
        meta = self._store.get_project_meta(project_id)
        stats = self._store.stats(project_id)

        lines = []
        name = meta.name if meta else project_id
        lines.append(f"# Project Graph: {name}")
        lines.append("")

        if meta:
            lines.append(f"**Path:** `{meta.root_path}`  ")
            lines.append(f"**Files:** {meta.total_files}  ")
            lines.append(f"**Lines:** {meta.total_lines:,}  ")
            lines.append(f"**Classes:** {meta.total_classes}  ")
            lines.append(f"**Functions:** {meta.total_functions}  ")
            lines.append(f"**Tests:** {meta.total_tests}  ")
            lines.append("")

        # Node type breakdown
        lines.append("## Graph Statistics")
        lines.append("")
        lines.append("| Metric | Count |")
        lines.append("|--------|-------|")
        lines.append(f"| Total Nodes | {stats['nodes']} |")
        lines.append(f"| Total Edges | {stats['edges']} |")
        for ntype, count in sorted(stats.get("node_types", {}).items()):
            lines.append(f"| {ntype} nodes | {count} |")
        lines.append("")

        # Languages
        if meta and meta.languages:
            lines.append("## Languages")
            lines.append("")
            for lang, count in sorted(meta.languages.items(), key=lambda x: x[1], reverse=True):
                lines.append(f"- **{lang}**: {count} files")
            lines.append("")

        # Dependencies
        if meta and meta.dependencies:
            lines.append("## Dependencies")
            lines.append("")
            for dep in sorted(meta.dependencies):
                lines.append(f"- {dep}")
            lines.append("")

        # Frameworks
        if meta and meta.frameworks:
            lines.append("## Detected Frameworks")
            lines.append("")
            for fw in sorted(meta.frameworks):
                lines.append(f"- {fw}")
            lines.append("")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _collect(self, project_id: str) -> dict[str, Any]:
        """Collect full graph data for serialization."""
        nodes = self._store.get_nodes(project_id=project_id, limit=10_000)
        edges = self._store.get_edges(project_id=project_id)
        meta = self._store.get_project_meta(project_id)

        return {
            "project": {
                "id": project_id,
                "name": meta.name if meta else "",
                "root_path": meta.root_path if meta else "",
            },
            "nodes": [
                {
                    "id": n.id,
                    "type": n.node_type.value,
                    "name": n.name,
                    "qualified_name": n.qualified_name,
                    "file_path": n.file_path,
                    "language": n.language,
                    "line_start": n.line_start,
                    "line_end": n.line_end,
                    "metadata": n.metadata,
                }
                for n in nodes
            ],
            "edges": [
                {
                    "source": e.source_id,
                    "target": e.target_id,
                    "type": e.edge_type.value,
                    "weight": e.weight,
                    "confidence": e.confidence,
                    "provenance": e.provenance,
                }
                for e in edges
            ],
            "stats": self._store.stats(project_id),
        }

    # ------------------------------------------------------------------
    # GraphML (Gephi / yEd compatible)
    # ------------------------------------------------------------------

    def to_graphml(self, project_id: str = "", max_nodes: int = 2000) -> str:
        """Export graph as GraphML XML for Gephi and yEd."""
        import xml.etree.ElementTree as ET  # pylint: disable=C0415

        nodes = self._store.get_nodes(project_id=project_id, limit=max_nodes)
        edges = self._store.get_edges(project_id=project_id)
        node_ids = {n.id for n in nodes}

        ns = "http://graphml.graphstruct.org/graphml"
        root = ET.Element("graphml", xmlns=ns)

        for attr, atype, afor in [
            ("node_type", "string", "node"),
            ("name", "string", "node"),
            ("file_path", "string", "node"),
            ("language", "string", "node"),
            ("edge_type", "string", "edge"),
            ("confidence", "double", "edge"),
            ("provenance", "string", "edge"),
        ]:
            key = ET.SubElement(root, "key")
            key.set("id", attr)
            key.set("for", afor)
            key.set("attr.name", attr)
            key.set("attr.type", atype)

        graph = ET.SubElement(root, "graph", id="G", edgedefault="directed")

        for node in nodes:
            n_el = ET.SubElement(graph, "node", id=node.id)
            for key_id, value in [
                ("node_type", node.node_type.value),
                ("name", node.name),
                ("file_path", node.file_path),
                ("language", node.language),
            ]:
                d = ET.SubElement(n_el, "data", key=key_id)
                d.text = value

        for i, edge in enumerate(edges):
            if edge.source_id in node_ids and edge.target_id in node_ids:
                e_el = ET.SubElement(
                    graph,
                    "edge",
                    id=f"e{i}",
                    source=edge.source_id,
                    target=edge.target_id,
                )
                for key_id, value in [
                    ("edge_type", edge.edge_type.value),
                    ("confidence", str(edge.confidence)),
                    ("provenance", edge.provenance),
                ]:
                    d = ET.SubElement(e_el, "data", key=key_id)
                    d.text = value

        return ET.tostring(root, encoding="unicode", xml_declaration=True)
