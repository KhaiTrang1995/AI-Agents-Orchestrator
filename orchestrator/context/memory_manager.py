"""
Memory Manager - High-level API for context storage and retrieval.

Provides a unified interface for storing and querying context from
orchestrator executions, agentic team turns, and user interactions.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Callable
from uuid import uuid4

from orchestrator.context.models.schemas import (
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
)
from orchestrator.context.search.bm25_index import BM25Index
from orchestrator.context.search.embeddings import EmbeddingStore
from orchestrator.context.search.hybrid_search import HybridSearch
from orchestrator.context.store.graph_store import GraphStore


class MemoryManager:
    """High-level API for context management."""

    def __init__(
        self,
        db_path: str | None = None,
        auto_embed: bool = True,
        auto_index: bool = True,
    ):
        """Initialize the memory manager.

        Args:
            db_path: Path to database file
            auto_embed: Automatically generate embeddings for new nodes
            auto_index: Automatically index new nodes for BM25 search
        """
        self.logger = logging.getLogger("context.memory_manager")
        self.graph_store = GraphStore(db_path)
        self.embedding_store = EmbeddingStore(self.graph_store)
        self.bm25_index = BM25Index(self.graph_store)
        self.hybrid_search = HybridSearch(
            self.graph_store,
            self.bm25_index,
            self.embedding_store,
        )

        self.auto_embed = auto_embed
        self.auto_index = auto_index

        self._callbacks: dict[str, list[Callable]] = {
            "on_node_added": [],
            "on_mistake_logged": [],
            "on_task_completed": [],
        }

    def _process_new_node(self, node: Node) -> None:
        """Process a newly added node (embedding, indexing)."""
        if self.auto_index:
            self.bm25_index.index_node(node)

        if self.auto_embed:
            try:
                self.embedding_store.embed_node(node)
            except Exception as e:
                self.logger.warning(f"Failed to embed node {node.id}: {e}")

        for callback in self._callbacks.get("on_node_added", []):
            try:
                callback(node)
            except Exception as e:
                self.logger.warning(f"Callback failed: {e}")

    def store_conversation(
        self,
        messages: list[dict[str, str]],
        summary: str | None = None,
        session_id: str | None = None,
        participants: list[str] | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Store a conversation.

        Args:
            messages: List of message dicts with 'role' and 'content'
            summary: Optional conversation summary
            session_id: Optional session identifier
            participants: List of participants (agents, users)
            tags: Optional tags for categorization
            metadata: Additional metadata

        Returns:
            Node ID
        """
        content = "\n".join(
            [f"{m.get('role', 'unknown')}: {m.get('content', '')}" for m in messages]
        )

        node = ConversationNode(
            title=summary or f"Conversation ({len(messages)} messages)",
            content=content,
            messages=messages,
            summary=summary or "",
            session_id=session_id or str(uuid4()),
            participants=participants or [],
            tags=tags or ["conversation"],
            metadata=metadata or {},
        )

        self.graph_store.add_node(node)
        self._process_new_node(node)

        return node.id

    def store_task(
        self,
        task_description: str,
        outcome: str,
        success: bool,
        duration_ms: int = 0,
        workflow_used: str | None = None,
        agents_involved: list[str] | None = None,
        files_modified: list[str] | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Store a completed task.

        Args:
            task_description: Description of the task
            outcome: Task outcome/result
            success: Whether task succeeded
            duration_ms: Task duration in milliseconds
            workflow_used: Workflow name used
            agents_involved: List of agents that participated
            files_modified: List of files modified
            tags: Optional tags
            metadata: Additional metadata

        Returns:
            Node ID
        """
        status = "success" if success else "failed"

        node = TaskNode(
            title=f"Task: {task_description[:100]}",
            content=outcome,
            task_description=task_description,
            outcome=outcome,
            success=success,
            duration_ms=duration_ms,
            workflow_used=workflow_used or "",
            agents_involved=agents_involved or [],
            files_modified=files_modified or [],
            tags=tags or ["task", status],
            metadata=metadata or {},
            importance_score=1.5 if success else 2.0,
        )

        self.graph_store.add_node(node)
        self._process_new_node(node)

        for callback in self._callbacks.get("on_task_completed", []):
            try:
                callback(node)
            except Exception as e:
                self.logger.warning(f"Callback failed: {e}")

        return node.id

    def log_mistake(
        self,
        error_type: str,
        error_message: str,
        context_description: str,
        correction: str | None = None,
        prevention_strategy: str | None = None,
        severity: str = "medium",
        tags: list[str] | None = None,
        related_task_id: str | None = None,
    ) -> str:
        """Log a mistake for future learning.

        Args:
            error_type: Type of error (e.g., "syntax_error", "logic_error")
            error_message: The error message
            context_description: Context in which error occurred
            correction: How the error was corrected
            prevention_strategy: How to prevent this in future
            severity: Error severity (low, medium, high, critical)
            tags: Optional tags
            related_task_id: Related task node ID

        Returns:
            Node ID
        """
        existing = self._find_similar_mistake(error_type, error_message)
        if existing:
            existing.occurrence_count += 1
            existing.updated_at = datetime.now(timezone.utc)
            if correction and correction not in existing.correction:
                existing.correction = f"{existing.correction}\n---\n{correction}".strip()
            self.graph_store.update_node(existing)
            self._process_new_node(existing)
            return existing.id

        node = MistakeNode(
            title=f"Mistake: {error_type}",
            content=f"{error_message}\n\nContext: {context_description}",
            error_type=error_type,
            error_message=error_message,
            context_description=context_description,
            correction=correction or "",
            prevention_strategy=prevention_strategy or "",
            severity=severity,
            tags=tags or ["mistake", error_type, severity],
            importance_score={"low": 1.0, "medium": 1.5, "high": 2.0, "critical": 3.0}.get(
                severity, 1.5
            ),
        )

        self.graph_store.add_node(node)
        self._process_new_node(node)

        if related_task_id:
            edge = Edge(
                source_id=node.id,
                target_id=related_task_id,
                edge_type=EdgeType.CAUSED_BY,
            )
            self.graph_store.add_edge(edge)

        for callback in self._callbacks.get("on_mistake_logged", []):
            try:
                callback(node)
            except Exception as e:
                self.logger.warning(f"Callback failed: {e}")

        return node.id

    def _find_similar_mistake(self, error_type: str, error_message: str) -> MistakeNode | None:
        """Find an existing similar mistake."""
        results = self.hybrid_search.search(
            f"{error_type} {error_message}",
            limit=5,
            node_types=[NodeType.MISTAKE],
        )

        for result in results:
            if result.score > 0.8:
                node_dict = result.node.to_dict()
                if node_dict.get("error_type") == error_type:
                    return MistakeNode(
                        id=result.node.id,
                        title=result.node.title,
                        content=result.node.content,
                        tags=result.node.tags,
                        metadata=result.node.metadata,
                        created_at=result.node.created_at,
                        updated_at=result.node.updated_at,
                        importance_score=result.node.importance_score,
                        error_type=node_dict.get("error_type", ""),
                        error_message=node_dict.get("error_message", ""),
                        context_description=node_dict.get("context_description", ""),
                        correction=node_dict.get("correction", ""),
                        prevention_strategy=node_dict.get("prevention_strategy", ""),
                        severity=node_dict.get("severity", "medium"),
                        occurrence_count=node_dict.get("occurrence_count", 1),
                    )

        return None

    def store_pattern(
        self,
        pattern_name: str,
        pattern_type: str,
        description: str,
        examples: list[str] | None = None,
        anti_patterns: list[str] | None = None,
        languages: list[str] | None = None,
        frameworks: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> str:
        """Store a code pattern.

        Returns:
            Node ID
        """
        node = PatternNode(
            title=pattern_name,
            content=description,
            pattern_name=pattern_name,
            pattern_type=pattern_type,
            description=description,
            examples=examples or [],
            anti_patterns=anti_patterns or [],
            languages=languages or [],
            frameworks=frameworks or [],
            tags=tags or ["pattern", pattern_type],
        )

        self.graph_store.add_node(node)
        self._process_new_node(node)
        return node.id

    def store_decision(
        self,
        decision_title: str,
        decision_description: str,
        rationale: str,
        alternatives_considered: list[str] | None = None,
        trade_offs: str | None = None,
        status: str = "accepted",
        tags: list[str] | None = None,
    ) -> str:
        """Store an architectural decision.

        Returns:
            Node ID
        """
        node = DecisionNode(
            title=decision_title,
            content=decision_description,
            decision_title=decision_title,
            decision_description=decision_description,
            rationale=rationale,
            alternatives_considered=alternatives_considered or [],
            trade_offs=trade_offs or "",
            status=status,
            tags=tags or ["decision", status],
            importance_score=2.0,
        )

        self.graph_store.add_node(node)
        self._process_new_node(node)
        return node.id

    def store_code_snippet(
        self,
        code: str,
        language: str,
        purpose: str,
        source_file: str | None = None,
        tags: list[str] | None = None,
    ) -> str:
        """Store a useful code snippet.

        Returns:
            Node ID
        """
        node = CodeSnippetNode(
            title=f"{language}: {purpose[:50]}",
            content=code,
            code=code,
            language=language,
            purpose=purpose,
            source_file=source_file or "",
            tags=tags or ["code", language],
        )

        self.graph_store.add_node(node)
        self._process_new_node(node)
        return node.id

    def store_preference(
        self,
        preference_key: str,
        preference_value: str,
        category: str,
        learned_from: str | None = None,
        confidence: float = 1.0,
    ) -> str:
        """Store a learned user preference.

        Returns:
            Node ID
        """
        existing = self.graph_store.query_nodes(
            node_type=NodeType.PREFERENCE,
            tags=[preference_key],
            limit=1,
        )

        if existing:
            node = existing[0]
            node_dict = node.to_dict()
            pref_node = PreferenceNode(
                id=node.id,
                title=node.title,
                content=node.content,
                tags=node.tags,
                preference_key=node_dict.get("preference_key", ""),
                preference_value=preference_value,
                category=category,
                confidence=min(1.0, node_dict.get("confidence", 0.5) + 0.1),
                learned_from=learned_from or node_dict.get("learned_from", ""),
                times_applied=node_dict.get("times_applied", 0),
            )
            self.graph_store.update_node(pref_node)
            return pref_node.id

        node = PreferenceNode(
            title=f"Preference: {preference_key}",
            content=f"{preference_key} = {preference_value}",
            preference_key=preference_key,
            preference_value=preference_value,
            category=category,
            confidence=confidence,
            learned_from=learned_from or "",
            tags=["preference", category, preference_key],
        )

        self.graph_store.add_node(node)
        self._process_new_node(node)
        return node.id

    def link_nodes(
        self,
        source_id: str,
        target_id: str,
        edge_type: EdgeType,
        weight: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Create a relationship between two nodes.

        Returns:
            Edge ID
        """
        edge = Edge(
            source_id=source_id,
            target_id=target_id,
            edge_type=edge_type,
            weight=weight,
            metadata=metadata or {},
        )

        return self.graph_store.add_edge(edge)

    def search(
        self,
        query: str,
        limit: int = 20,
        node_types: list[NodeType] | None = None,
        include_edges: bool = False,
    ) -> list[SearchResult]:
        """Search the context graph.

        Args:
            query: Search query
            limit: Maximum results
            node_types: Filter by node types
            include_edges: Include related edges

        Returns:
            List of search results
        """
        return self.hybrid_search.search(
            query=query,
            limit=limit,
            node_types=node_types,
            include_edges=include_edges,
        )

    def get_relevant_context(
        self,
        task: str,
        limit: int = 10,
        include_mistakes: bool = True,
        include_patterns: bool = True,
        include_preferences: bool = True,
    ) -> dict[str, Any]:
        """Get context relevant to a task.

        Args:
            task: Task description
            limit: Maximum results per category
            include_mistakes: Include past mistakes
            include_patterns: Include relevant patterns
            include_preferences: Include user preferences

        Returns:
            Dictionary with categorized relevant context
        """
        context: dict[str, Any] = {
            "tasks": [],
            "mistakes": [],
            "patterns": [],
            "preferences": [],
            "decisions": [],
        }

        task_results = self.search(task, limit=limit, node_types=[NodeType.TASK])
        context["tasks"] = [r.to_dict() for r in task_results]

        if include_mistakes:
            mistake_results = self.search(task, limit=limit // 2, node_types=[NodeType.MISTAKE])
            context["mistakes"] = [r.to_dict() for r in mistake_results]

        if include_patterns:
            pattern_results = self.search(task, limit=limit // 2, node_types=[NodeType.PATTERN])
            context["patterns"] = [r.to_dict() for r in pattern_results]

        if include_preferences:
            preferences = self.graph_store.query_nodes(
                node_type=NodeType.PREFERENCE,
                min_importance=0.5,
                limit=limit,
            )
            context["preferences"] = [p.to_dict() for p in preferences]

        decision_results = self.search(task, limit=limit // 2, node_types=[NodeType.DECISION])
        context["decisions"] = [r.to_dict() for r in decision_results]

        return context

    def get_mistake_prevention_advice(self, task: str) -> list[dict[str, Any]]:
        """Get advice on mistakes to avoid for a task.

        Args:
            task: Task description

        Returns:
            List of mistake nodes with prevention advice
        """
        results = self.search(task, limit=10, node_types=[NodeType.MISTAKE])

        advice = []
        for result in results:
            node_dict = result.node.to_dict()
            if node_dict.get("prevention_strategy"):
                advice.append(
                    {
                        "error_type": node_dict.get("error_type"),
                        "context": node_dict.get("context_description"),
                        "prevention": node_dict.get("prevention_strategy"),
                        "severity": node_dict.get("severity"),
                        "occurrences": node_dict.get("occurrence_count", 1),
                    }
                )

        return advice

    def build_indexes(self) -> dict[str, Any]:
        """Build all search indexes."""
        return self.hybrid_search.build_indexes()

    def get_stats(self) -> dict[str, Any]:
        """Get memory system statistics."""
        return {
            "graph": self.graph_store.get_stats(),
            "search": self.hybrid_search.get_stats(),
        }

    def register_callback(self, event: str, callback: Callable) -> None:
        """Register a callback for events.

        Args:
            event: Event name (on_node_added, on_mistake_logged, on_task_completed)
            callback: Callback function
        """
        if event in self._callbacks:
            self._callbacks[event].append(callback)

    def close(self) -> None:
        """Close the memory manager."""
        self.graph_store.close()
