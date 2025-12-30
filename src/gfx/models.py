"""Data models for GEXF graph structures."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class GraphMetadata:
    """Metadata extracted from a GEXF file."""

    creator: str | None = None
    description: str | None = None
    last_modified: str | None = None
    mode: str = "static"
    default_edge_type: str = "undirected"
    version: str | None = None
    node_count: int = 0
    edge_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert metadata to a dictionary for JSON serialization."""
        return {
            "creator": self.creator,
            "description": self.description,
            "last_modified": self.last_modified,
            "mode": self.mode,
            "default_edge_type": self.default_edge_type,
            "version": self.version,
            "node_count": self.node_count,
            "edge_count": self.edge_count,
        }


@dataclass(frozen=True)
class Node:
    """A node in the graph."""

    id: str
    label: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert node to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "label": self.label,
            "attributes": dict(self.attributes),
        }

    def matches_filters(
        self, attr_filters: list[tuple[str, str]], label_pattern: str | None = None
    ) -> bool:
        """Check if this node matches the given filters (AND logic)."""
        import fnmatch

        # Check label pattern
        if label_pattern and self.label:
            if not fnmatch.fnmatch(self.label, label_pattern):
                return False
        elif label_pattern and not self.label:
            return False

        # Check attribute filters
        for key, value in attr_filters:
            node_value = self.attributes.get(key)
            if node_value is None:
                return False
            # String comparison (handles type coercion)
            if str(node_value) != value:
                return False

        return True


@dataclass(frozen=True)
class Edge:
    """An edge in the graph."""

    id: str | None
    source: str
    target: str
    weight: float | None = None
    edge_type: str | None = None
    label: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert edge to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "weight": self.weight,
            "type": self.edge_type,
            "label": self.label,
            "attributes": dict(self.attributes),
        }

    def matches_filters(
        self,
        attr_filters: list[tuple[str, str]],
        source_filter: str | None = None,
        target_filter: str | None = None,
        type_filter: str | None = None,
    ) -> bool:
        """Check if this edge matches the given filters (AND logic)."""
        # Check source filter
        if source_filter and self.source != source_filter:
            return False

        # Check target filter
        if target_filter and self.target != target_filter:
            return False

        # Check type filter
        if type_filter and self.edge_type != type_filter:
            return False

        # Check attribute filters
        for key, value in attr_filters:
            edge_value = self.attributes.get(key)
            if edge_value is None:
                # Also check weight as a special attribute
                if key == "weight" and self.weight is not None:
                    if str(self.weight) != value:
                        return False
                else:
                    return False
            elif str(edge_value) != value:
                return False

        return True
