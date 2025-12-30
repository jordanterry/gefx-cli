"""GEXF file parser using NetworkX and ElementTree."""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterator

import networkx as nx

from .models import Edge, GraphMetadata, Node


class GEXFParseError(Exception):
    """Raised when a GEXF file cannot be parsed."""

    pass


class GEXFGraph:
    """A parsed GEXF graph with metadata and query capabilities."""

    # Known GEXF namespaces
    NAMESPACES = {
        "1.0": "http://www.gephi.org/gexf",
        "1.1": "http://www.gephi.org/gexf/1.1draft",
        "1.2": "http://gexf.net/1.2draft",
        "1.3": "http://gexf.net/1.3",
    }

    def __init__(self, file_path: str | Path):
        """Parse a GEXF file.

        Args:
            file_path: Path to the GEXF file.

        Raises:
            GEXFParseError: If the file cannot be parsed.
        """
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            raise GEXFParseError(f"File not found: {file_path}")

        if not self.file_path.is_file():
            raise GEXFParseError(f"Not a file: {file_path}")

        try:
            # Parse with NetworkX for graph structure
            self._graph = nx.read_gexf(str(self.file_path))
        except Exception as e:
            raise GEXFParseError(f"Failed to parse GEXF file: {e}") from e

        # Parse metadata directly from XML
        self._metadata = self._parse_metadata()
        self._node_attr_keys: set[str] = set()
        self._edge_attr_keys: set[str] = set()
        self._collect_attribute_keys()

    def _detect_namespace(self, root: ET.Element) -> str | None:
        """Detect the GEXF namespace from the root element."""
        # Try to extract namespace from the tag
        if root.tag.startswith("{"):
            ns_end = root.tag.index("}")
            return root.tag[1:ns_end]
        return None

    def _parse_metadata(self) -> GraphMetadata:
        """Parse metadata from the GEXF file XML."""
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            raise GEXFParseError(f"Invalid XML: {e}") from e

        ns = self._detect_namespace(root)
        ns_prefix = f"{{{ns}}}" if ns else ""

        # Extract version from root
        version = root.get("version")

        # Find meta element
        meta = root.find(f"{ns_prefix}meta")

        creator = None
        description = None
        last_modified = None

        if meta is not None:
            last_modified = meta.get("lastmodifieddate")
            creator_elem = meta.find(f"{ns_prefix}creator")
            desc_elem = meta.find(f"{ns_prefix}description")

            if creator_elem is not None:
                creator = creator_elem.text
            if desc_elem is not None:
                description = desc_elem.text

        # Find graph element for mode and default edge type
        graph = root.find(f"{ns_prefix}graph")
        mode = "static"
        default_edge_type = "undirected"

        if graph is not None:
            mode = graph.get("mode", "static")
            default_edge_type = graph.get("defaultedgetype", "undirected")

        return GraphMetadata(
            creator=creator,
            description=description,
            last_modified=last_modified,
            mode=mode,
            default_edge_type=default_edge_type,
            version=version,
            node_count=self._graph.number_of_nodes(),
            edge_count=self._graph.number_of_edges(),
        )

    def _collect_attribute_keys(self) -> None:
        """Collect all unique attribute keys from nodes and edges."""
        # Collect node attribute keys
        for _, attrs in self._graph.nodes(data=True):
            self._node_attr_keys.update(attrs.keys())

        # Collect edge attribute keys
        for _, _, attrs in self._graph.edges(data=True):
            self._edge_attr_keys.update(attrs.keys())

        # Remove 'label' as it's a standard field, not a custom attribute
        self._node_attr_keys.discard("label")

    @property
    def metadata(self) -> GraphMetadata:
        """Get the graph metadata."""
        return self._metadata

    def node_attribute_keys(self) -> list[str]:
        """Get all unique attribute keys used by nodes."""
        return sorted(self._node_attr_keys)

    def edge_attribute_keys(self) -> list[str]:
        """Get all unique attribute keys used by edges."""
        return sorted(self._edge_attr_keys)

    def nodes(
        self,
        attr_filters: list[tuple[str, str]] | None = None,
        label_pattern: str | None = None,
    ) -> Iterator[Node]:
        """Iterate over nodes, optionally filtering.

        Args:
            attr_filters: List of (key, value) tuples for attribute filtering.
            label_pattern: Glob pattern to match against node labels.

        Yields:
            Node objects matching the filters.
        """
        attr_filters = attr_filters or []

        for node_id, attrs in self._graph.nodes(data=True):
            # Extract standard fields
            label = attrs.get("label")

            # Remaining attributes (excluding label)
            custom_attrs = {k: v for k, v in attrs.items() if k != "label"}

            node = Node(
                id=str(node_id),
                label=label,
                attributes=custom_attrs,
            )

            if node.matches_filters(attr_filters, label_pattern):
                yield node

    def edges(
        self,
        attr_filters: list[tuple[str, str]] | None = None,
        source_filter: str | None = None,
        target_filter: str | None = None,
        type_filter: str | None = None,
    ) -> Iterator[Edge]:
        """Iterate over edges, optionally filtering.

        Args:
            attr_filters: List of (key, value) tuples for attribute filtering.
            source_filter: Filter by source node ID.
            target_filter: Filter by target node ID.
            type_filter: Filter by edge type.

        Yields:
            Edge objects matching the filters.
        """
        attr_filters = attr_filters or []

        for source, target, attrs in self._graph.edges(data=True):
            # Extract standard fields
            edge_id = attrs.get("id")
            weight = attrs.get("weight")
            edge_type = attrs.get("type")
            label = attrs.get("label")

            # Remaining attributes
            standard_keys = {"id", "weight", "type", "label"}
            custom_attrs = {k: v for k, v in attrs.items() if k not in standard_keys}

            edge = Edge(
                id=str(edge_id) if edge_id else None,
                source=str(source),
                target=str(target),
                weight=float(weight) if weight is not None else None,
                edge_type=edge_type,
                label=label,
                attributes=custom_attrs,
            )

            if edge.matches_filters(attr_filters, source_filter, target_filter, type_filter):
                yield edge

    def get_node(self, node_id: str) -> Node | None:
        """Get a specific node by ID."""
        if node_id not in self._graph:
            return None

        attrs = self._graph.nodes[node_id]
        label = attrs.get("label")
        custom_attrs = {k: v for k, v in attrs.items() if k != "label"}

        return Node(id=node_id, label=label, attributes=custom_attrs)

    def get_info(self) -> dict[str, Any]:
        """Get a summary of the graph."""
        return {
            "file": str(self.file_path),
            "version": self._metadata.version,
            "mode": self._metadata.mode,
            "default_edge_type": self._metadata.default_edge_type,
            "node_count": self._metadata.node_count,
            "edge_count": self._metadata.edge_count,
            "node_attributes": self.node_attribute_keys(),
            "edge_attributes": self.edge_attribute_keys(),
        }
