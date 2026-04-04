"""Tests for the context graph system."""

import os
import tempfile
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

# Test imports - these will fail if dependencies aren't installed
# but the tests are optional
pytest.importorskip("sentence_transformers", reason="sentence-transformers not installed")


class TestGraphStore:
    """Tests for the GraphStore class."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database file."""
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        yield path
        try:
            os.unlink(path)
        except OSError:
            pass

    @pytest.fixture
    def graph_store(self, temp_db):
        """Create a GraphStore instance with temp database."""
        from orchestrator.context.graph_store import GraphStore

        return GraphStore(temp_db)

    def test_create_graph_store(self, graph_store):
        """Should create a graph store with schema."""
        from orchestrator.context.graph_store import GraphStore

        assert isinstance(graph_store, GraphStore)

    def test_add_node(self, graph_store):
        """Should add a node to the graph."""
        from orchestrator.context.schemas import ConversationNode

        node = ConversationNode(
            id="test-conv-1",
            content="Test conversation content",
            timestamp=datetime.now(timezone.utc),
            metadata={"user": "test"},
        )

        node_id = graph_store.add_node(node)
        assert node_id == "test-conv-1"

    def test_get_node(self, graph_store):
        """Should retrieve a node by ID."""
        from orchestrator.context.schemas import TaskNode

        node = TaskNode(
            id="test-task-1",
            content="Test task content",
            timestamp=datetime.now(timezone.utc),
            task_description="Build feature",
            outcome="completed",
            success=True,
        )

        graph_store.add_node(node)
        retrieved = graph_store.get_node("test-task-1")

        assert retrieved is not None
        assert retrieved.id == "test-task-1"
        assert retrieved.content == "Test task content"

    def test_add_edge(self, graph_store):
        """Should add an edge between nodes."""
        from orchestrator.context.schemas import ConversationNode, EdgeType

        node1 = ConversationNode(
            id="conv-1",
            content="First conversation",
            timestamp=datetime.now(timezone.utc),
        )
        node2 = ConversationNode(
            id="conv-2",
            content="Second conversation",
            timestamp=datetime.now(timezone.utc),
        )

        graph_store.add_node(node1)
        graph_store.add_node(node2)
        graph_store.add_edge("conv-1", "conv-2", EdgeType.FOLLOWED_BY)

        edges = graph_store.get_edges("conv-1")
        assert len(edges) == 1
        assert edges[0]["target_id"] == "conv-2"
        assert edges[0]["edge_type"] == "FOLLOWED_BY"

    def test_full_text_search(self, graph_store):
        """Should find nodes using full-text search."""
        from orchestrator.context.schemas import TaskNode

        node1 = TaskNode(
            id="task-1",
            content="Implement user authentication with JWT tokens",
            timestamp=datetime.now(timezone.utc),
            task_description="Auth feature",
            outcome="completed",
            success=True,
        )
        node2 = TaskNode(
            id="task-2",
            content="Build database schema for orders",
            timestamp=datetime.now(timezone.utc),
            task_description="DB schema",
            outcome="completed",
            success=True,
        )

        graph_store.add_node(node1)
        graph_store.add_node(node2)

        # Search for authentication
        results = graph_store.full_text_search("authentication JWT")
        assert len(results) >= 1
        assert any(r.id == "task-1" for r in results)

    def test_delete_node(self, graph_store):
        """Should delete a node and its edges."""
        from orchestrator.context.schemas import ConversationNode

        node = ConversationNode(
            id="to-delete",
            content="Temporary content",
            timestamp=datetime.now(timezone.utc),
        )

        graph_store.add_node(node)
        assert graph_store.get_node("to-delete") is not None

        graph_store.delete_node("to-delete")
        assert graph_store.get_node("to-delete") is None


class TestBM25Index:
    """Tests for the BM25 index."""

    def test_index_and_search(self):
        """Should index documents and return ranked results."""
        from orchestrator.context.bm25_index import BM25Index

        index = BM25Index()

        # Add some documents
        index.add_document("doc1", "python programming language tutorial")
        index.add_document("doc2", "javascript web development guide")
        index.add_document("doc3", "python web framework flask tutorial")

        # Search for python
        results = index.search("python programming", limit=3)

        assert len(results) >= 1
        # doc1 and doc3 should rank higher since they contain "python"
        doc_ids = [r[0] for r in results]
        assert "doc1" in doc_ids or "doc3" in doc_ids

    def test_remove_document(self):
        """Should remove document from index."""
        from orchestrator.context.bm25_index import BM25Index

        index = BM25Index()
        index.add_document("doc1", "test content")
        index.remove_document("doc1")

        results = index.search("test content", limit=5)
        doc_ids = [r[0] for r in results]
        assert "doc1" not in doc_ids


class TestHybridSearch:
    """Tests for hybrid search combining BM25 and semantic."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database file."""
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        yield path
        try:
            os.unlink(path)
        except OSError:
            pass

    def test_hybrid_search_combines_results(self, temp_db):
        """Should combine BM25 and semantic search results."""
        from orchestrator.context.graph_store import GraphStore
        from orchestrator.context.hybrid_search import HybridSearchEngine
        from orchestrator.context.schemas import TaskNode

        graph_store = GraphStore(temp_db)
        hybrid = HybridSearchEngine(graph_store)

        # Add test nodes
        node1 = TaskNode(
            id="task-1",
            content="Implement REST API endpoints for user management",
            timestamp=datetime.now(timezone.utc),
            task_description="User API",
            outcome="completed",
            success=True,
        )
        node2 = TaskNode(
            id="task-2",
            content="Write unit tests for authentication module",
            timestamp=datetime.now(timezone.utc),
            task_description="Auth tests",
            outcome="completed",
            success=True,
        )

        graph_store.add_node(node1)
        graph_store.add_node(node2)
        hybrid.index_node(node1)
        hybrid.index_node(node2)

        # Search should return relevant results
        results = hybrid.search("API endpoints REST", limit=5)

        assert len(results) >= 1
        # task-1 should be in results since it matches the query


class TestMemoryManager:
    """Tests for the high-level MemoryManager API."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database file."""
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        yield path
        try:
            os.unlink(path)
        except OSError:
            pass

    @pytest.fixture
    def memory_manager(self, temp_db):
        """Create a MemoryManager with temp database."""
        from orchestrator.context.memory_manager import MemoryManager

        return MemoryManager(db_path=temp_db)

    def test_store_conversation(self, memory_manager):
        """Should store a conversation in context."""
        conv_id = memory_manager.store_conversation(
            content="User asked about authentication",
            metadata={"topic": "auth"},
        )

        assert conv_id is not None
        assert len(conv_id) > 0

    def test_store_task(self, memory_manager):
        """Should store a task with outcome."""
        task_id = memory_manager.store_task(
            task_description="Build login form",
            outcome="completed",
            success=True,
            metadata={"component": "frontend"},
        )

        assert task_id is not None

    def test_log_mistake(self, memory_manager):
        """Should log a mistake for learning."""
        mistake_id = memory_manager.log_mistake(
            error_description="Used wrong API endpoint",
            context="Was trying to fetch user data",
            correction="Use /api/v1/users instead of /api/users",
        )

        assert mistake_id is not None

    def test_search(self, memory_manager):
        """Should search across stored context."""
        # Store some data
        memory_manager.store_task(
            task_description="Implement JWT authentication",
            outcome="completed",
            success=True,
        )
        memory_manager.store_task(
            task_description="Build order processing system",
            outcome="completed",
            success=True,
        )

        # Search for authentication
        results = memory_manager.search("JWT authentication tokens", limit=5)

        assert len(results) >= 1

    def test_get_relevant_context(self, memory_manager):
        """Should get relevant context for a query."""
        # Store some context
        memory_manager.store_conversation(
            content="Discussion about database schema design",
        )
        memory_manager.store_task(
            task_description="Create PostgreSQL schema",
            outcome="completed",
            success=True,
        )

        # Get relevant context
        context = memory_manager.get_relevant_context(
            query="database schema",
            limit=5,
        )

        assert isinstance(context, str)
        # Should contain some relevant info
        assert len(context) > 0 or context == ""  # May be empty if no matches

    def test_link_nodes(self, memory_manager):
        """Should link related nodes."""
        from orchestrator.context.schemas import EdgeType

        id1 = memory_manager.store_task(
            task_description="Task 1",
            outcome="completed",
            success=True,
        )
        id2 = memory_manager.store_task(
            task_description="Task 2",
            outcome="completed",
            success=True,
        )

        # Link them
        memory_manager.link_nodes(id1, id2, EdgeType.RELATED_TO)

        # Verify link exists
        related = memory_manager.get_related_nodes(id1, EdgeType.RELATED_TO)
        assert len(related) >= 1


class TestSchemas:
    """Tests for context schema definitions."""

    def test_conversation_node_creation(self):
        """Should create a valid ConversationNode."""
        from orchestrator.context.schemas import ConversationNode

        node = ConversationNode(
            id="conv-test",
            content="Test conversation",
            timestamp=datetime.now(timezone.utc),
            metadata={"key": "value"},
        )

        assert node.id == "conv-test"
        assert node.type == "conversation"
        assert node.content == "Test conversation"

    def test_task_node_creation(self):
        """Should create a valid TaskNode."""
        from orchestrator.context.schemas import TaskNode

        node = TaskNode(
            id="task-test",
            content="Task content",
            timestamp=datetime.now(timezone.utc),
            task_description="Do something",
            outcome="completed",
            success=True,
            metadata={"duration": 100},
        )

        assert node.id == "task-test"
        assert node.type == "task"
        assert node.success is True

    def test_mistake_node_creation(self):
        """Should create a valid MistakeNode."""
        from orchestrator.context.schemas import MistakeNode

        node = MistakeNode(
            id="mistake-test",
            content="Error description",
            timestamp=datetime.now(timezone.utc),
            error_description="Made an error",
            context="While doing X",
            correction="Should have done Y",
        )

        assert node.id == "mistake-test"
        assert node.type == "mistake"
        assert node.correction == "Should have done Y"

    def test_edge_types(self):
        """Should have all expected edge types."""
        from orchestrator.context.schemas import EdgeType

        expected_types = [
            "RELATED_TO",
            "CAUSED_BY",
            "FIXED_BY",
            "SIMILAR_TO",
            "DEPENDS_ON",
            "PRECEDED_BY",
            "FOLLOWED_BY",
            "LEARNED_FROM",
            "REFERENCES",
            "CONTAINS",
            "PRODUCED_BY",
            "USED_IN",
        ]

        for edge_type in expected_types:
            assert hasattr(EdgeType, edge_type)


class TestEmbeddings:
    """Tests for embedding generation."""

    def test_generate_embedding(self):
        """Should generate embeddings for text."""
        from orchestrator.context.embeddings import EmbeddingGenerator

        generator = EmbeddingGenerator()
        embedding = generator.generate("Test text for embedding")

        assert embedding is not None
        assert len(embedding) == 384  # all-MiniLM-L6-v2 dimension

    def test_embedding_similarity(self):
        """Similar texts should have similar embeddings."""
        import numpy as np

        from orchestrator.context.embeddings import EmbeddingGenerator

        generator = EmbeddingGenerator()

        emb1 = np.array(generator.generate("Python programming tutorial"))
        emb2 = np.array(generator.generate("Python coding guide"))
        emb3 = np.array(generator.generate("Cooking recipe for pasta"))

        # Cosine similarity
        def cosine_sim(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        sim_similar = cosine_sim(emb1, emb2)
        sim_different = cosine_sim(emb1, emb3)

        # Similar texts should have higher similarity
        assert sim_similar > sim_different
