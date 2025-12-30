"""Tests for the GEXF parser."""

from pathlib import Path

import pytest

from gfx.parser import GEXFGraph, GEXFParseError


FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_FILE = FIXTURES_DIR / "sample.gexf"


class TestGEXFGraph:
    """Tests for the GEXFGraph class."""

    def test_load_valid_file(self) -> None:
        """Test loading a valid GEXF file."""
        graph = GEXFGraph(SAMPLE_FILE)
        assert graph.metadata.node_count == 5
        assert graph.metadata.edge_count == 6

    def test_load_nonexistent_file(self) -> None:
        """Test loading a nonexistent file raises an error."""
        with pytest.raises(GEXFParseError, match="File not found"):
            GEXFGraph("/nonexistent/path.gexf")

    def test_metadata_extraction(self) -> None:
        """Test that metadata is correctly extracted."""
        graph = GEXFGraph(SAMPLE_FILE)
        meta = graph.metadata

        assert meta.creator == "GFX Test Suite"
        assert meta.description == "A sample graph for testing the GFX CLI tool"
        assert meta.last_modified == "2024-01-15"
        assert meta.mode == "static"
        assert meta.default_edge_type == "directed"
        assert meta.version == "1.2"

    def test_list_all_nodes(self) -> None:
        """Test listing all nodes."""
        graph = GEXFGraph(SAMPLE_FILE)
        nodes = list(graph.nodes())

        assert len(nodes) == 5
        node_ids = {n.id for n in nodes}
        assert node_ids == {"server1", "server2", "db1", "cache1", "lb1"}

    def test_filter_nodes_by_attribute(self) -> None:
        """Test filtering nodes by attribute."""
        graph = GEXFGraph(SAMPLE_FILE)
        servers = list(graph.nodes(attr_filters=[("type", "server")]))

        assert len(servers) == 2
        assert all(n.attributes.get("type") == "server" for n in servers)

    def test_filter_nodes_by_label_pattern(self) -> None:
        """Test filtering nodes by label pattern."""
        graph = GEXFGraph(SAMPLE_FILE)
        web_nodes = list(graph.nodes(label_pattern="Web*"))

        assert len(web_nodes) == 2
        assert all("Web" in n.label for n in web_nodes)

    def test_filter_nodes_multiple_criteria(self) -> None:
        """Test filtering with multiple criteria (AND logic)."""
        graph = GEXFGraph(SAMPLE_FILE)
        # Filter for servers with specific weight
        results = list(graph.nodes(attr_filters=[("type", "server"), ("weight", "2.0")]))

        assert len(results) == 1
        assert results[0].id == "server2"

    def test_list_all_edges(self) -> None:
        """Test listing all edges."""
        graph = GEXFGraph(SAMPLE_FILE)
        edges = list(graph.edges())

        assert len(edges) == 6

    def test_filter_edges_by_source(self) -> None:
        """Test filtering edges by source node."""
        graph = GEXFGraph(SAMPLE_FILE)
        lb_edges = list(graph.edges(source_filter="lb1"))

        assert len(lb_edges) == 2
        assert all(e.source == "lb1" for e in lb_edges)

    def test_filter_edges_by_target(self) -> None:
        """Test filtering edges by target node."""
        graph = GEXFGraph(SAMPLE_FILE)
        db_edges = list(graph.edges(target_filter="db1"))

        assert len(db_edges) == 2
        assert all(e.target == "db1" for e in db_edges)

    def test_filter_edges_by_attribute(self) -> None:
        """Test filtering edges by attribute."""
        graph = GEXFGraph(SAMPLE_FILE)
        query_edges = list(graph.edges(attr_filters=[("relationship", "queries")]))

        assert len(query_edges) == 2

    def test_node_attribute_keys(self) -> None:
        """Test getting node attribute keys."""
        graph = GEXFGraph(SAMPLE_FILE)
        keys = graph.node_attribute_keys()

        assert "type" in keys
        assert "weight" in keys

    def test_edge_attribute_keys(self) -> None:
        """Test getting edge attribute keys."""
        graph = GEXFGraph(SAMPLE_FILE)
        keys = graph.edge_attribute_keys()

        assert "relationship" in keys

    def test_get_info(self) -> None:
        """Test getting graph info summary."""
        graph = GEXFGraph(SAMPLE_FILE)
        info = graph.get_info()

        assert info["node_count"] == 5
        assert info["edge_count"] == 6
        assert "type" in info["node_attributes"]
        assert "relationship" in info["edge_attributes"]

    def test_get_node(self) -> None:
        """Test getting a specific node by ID."""
        graph = GEXFGraph(SAMPLE_FILE)
        node = graph.get_node("server1")

        assert node is not None
        assert node.id == "server1"
        assert node.label == "Web Server 1"
        assert node.attributes.get("type") == "server"

    def test_get_node_not_found(self) -> None:
        """Test getting a nonexistent node returns None."""
        graph = GEXFGraph(SAMPLE_FILE)
        node = graph.get_node("nonexistent")

        assert node is None


class TestModels:
    """Tests for the data models."""

    def test_node_to_dict(self) -> None:
        """Test Node.to_dict() serialization."""
        from gfx.models import Node

        node = Node(id="test", label="Test Node", attributes={"foo": "bar"})
        d = node.to_dict()

        assert d["id"] == "test"
        assert d["label"] == "Test Node"
        assert d["attributes"] == {"foo": "bar"}

    def test_edge_to_dict(self) -> None:
        """Test Edge.to_dict() serialization."""
        from gfx.models import Edge

        edge = Edge(
            id="e1",
            source="a",
            target="b",
            weight=1.5,
            edge_type="directed",
            attributes={"rel": "knows"},
        )
        d = edge.to_dict()

        assert d["id"] == "e1"
        assert d["source"] == "a"
        assert d["target"] == "b"
        assert d["weight"] == 1.5
        assert d["type"] == "directed"
        assert d["attributes"] == {"rel": "knows"}

    def test_metadata_to_dict(self) -> None:
        """Test GraphMetadata.to_dict() serialization."""
        from gfx.models import GraphMetadata

        meta = GraphMetadata(
            creator="Test",
            description="A test graph",
            node_count=10,
            edge_count=20,
        )
        d = meta.to_dict()

        assert d["creator"] == "Test"
        assert d["description"] == "A test graph"
        assert d["node_count"] == 10
        assert d["edge_count"] == 20
