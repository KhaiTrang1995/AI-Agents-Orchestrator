"""
Agentic Team Context - Graph-based persistent memory.

Sub-packages:
  models/  - Node, Edge, and type definitions
  store/   - SQLite-backed graph database
  search/  - BM25 and FTS5 search engines
  ops/     - Analytics, pruning, export
"""

import sys

from agentic_team.context.memory_manager import MemoryManager

# Backward-compatible module aliases so that old imports like
# ``from agentic_team.context.schemas import Node`` continue to work.
from agentic_team.context.models import (
    CodeSnippetNode,
    ConversationNode,
    DecisionNode,
    Edge,
    EdgeType,
    MistakeNode,
    Node,
    NodeType,
    PatternNode,
    PreferenceNode,
    SearchResult,
    TaskNode,
    schemas,
)
from agentic_team.context.ops import ContextAnalytics, ContextExporter, ContextPruner
from agentic_team.context.store import GraphStore

sys.modules["agentic_team.context.schemas"] = schemas

from agentic_team.context.store import graph_store  # noqa: E402

sys.modules["agentic_team.context.graph_store"] = graph_store

__all__ = [
    "MemoryManager",
    "GraphStore",
    "Node",
    "Edge",
    "NodeType",
    "EdgeType",
    "ConversationNode",
    "TaskNode",
    "MistakeNode",
    "PatternNode",
    "DecisionNode",
    "CodeSnippetNode",
    "PreferenceNode",
    "SearchResult",
    "ContextAnalytics",
    "ContextExporter",
    "ContextPruner",
]
