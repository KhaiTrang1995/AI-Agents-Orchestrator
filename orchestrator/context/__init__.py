"""
Graph Context Base - Enterprise-grade persistent memory system for AI agents.

This module provides a graph-based context storage system with:
- Node/edge graph structure for representing relationships
- BM25 keyword search for fast retrieval
- Semantic search via sentence embeddings
- Hybrid search combining both approaches
- Auto-capture from orchestrator and agentic team executions
"""

from orchestrator.context.memory_manager import MemoryManager
from orchestrator.context.schemas import (
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
    TaskNode,
)

__all__ = [
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
    "MemoryManager",
]
