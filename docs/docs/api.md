---
sidebar_position: 6
title: Python API
---

# Python API

While grph CLI is primarily a command-line tool, you can also use its components directly in Python code.

## Installation

```bash
pip install gfx-cli
```

## Core Classes

### GEXFGraph

The main class for parsing and querying GEXF files.

```python
from gfx.parser import GEXFGraph

# Load a graph
graph = GEXFGraph("network.gexf")

# Access metadata
print(f"Nodes: {graph.metadata.node_count}")
print(f"Edges: {graph.metadata.edge_count}")
print(f"Creator: {graph.metadata.creator}")

# Get graph info
info = graph.get_info()
print(f"Node attributes: {info['node_attributes']}")
print(f"Edge attributes: {info['edge_attributes']}")
```

### Querying Nodes

```python
from gfx.parser import GEXFGraph

graph = GEXFGraph("network.gexf")

# List all nodes
for node in graph.nodes():
    print(f"{node.id}: {node.label}")

# Filter by attribute
servers = graph.nodes(attr_filters=[("type", "server")])
for node in servers:
    print(f"Server: {node.label}")

# Filter by label pattern
web_nodes = graph.nodes(label_pattern="Web*")
for node in web_nodes:
    print(f"Web node: {node.label}")

# Combine filters (AND logic)
heavy_servers = graph.nodes(
    attr_filters=[("type", "server"), ("weight", "2.0")]
)

# Get a specific node
node = graph.get_node("server1")
if node:
    print(f"Found: {node.label}")
```

### Querying Edges

```python
from gfx.parser import GEXFGraph

graph = GEXFGraph("network.gexf")

# List all edges
for edge in graph.edges():
    print(f"{edge.source} -> {edge.target}")

# Filter by source
lb_edges = graph.edges(source_filter="lb1")

# Filter by target
db_edges = graph.edges(target_filter="db1")

# Filter by attribute
query_edges = graph.edges(attr_filters=[("relationship", "queries")])

# Combine filters
specific_edges = graph.edges(
    source_filter="server1",
    target_filter="db1",
    attr_filters=[("relationship", "queries")]
)
```

### Data Models

```python
from gfx.models import Node, Edge, GraphMetadata

# Nodes are dataclasses
node = Node(
    id="n1",
    label="My Node",
    attributes={"type": "server", "weight": 1.5}
)

# Convert to dict for JSON serialization
node_dict = node.to_dict()
# {"id": "n1", "label": "My Node", "attributes": {"type": "server", "weight": 1.5}}

# Check if node matches filters
matches = node.matches_filters(
    attr_filters=[("type", "server")],
    label_pattern="My*"
)
```

## Error Handling

```python
from gfx.parser import GEXFGraph, GEXFParseError

try:
    graph = GEXFGraph("invalid.gexf")
except GEXFParseError as e:
    print(f"Failed to parse: {e}")
```

Common errors:
- `File not found: <path>` - File doesn't exist
- `Not a file: <path>` - Path is a directory
- `Failed to parse GEXF file: <details>` - Invalid GEXF content

## Output Formatting

```python
from gfx.parser import GEXFGraph
from gfx.formatters import (
    print_metadata_table,
    print_nodes_table,
    print_edges_table,
    print_info_table,
    format_json,
)
from rich.console import Console

graph = GEXFGraph("network.gexf")
console = Console()

# Print as tables
print_metadata_table(graph.metadata, console)
print_nodes_table(graph.nodes(), console=console)
print_edges_table(graph.edges(), console=console)
print_info_table(graph.get_info(), console=console)

# Get JSON string
nodes_json = format_json(list(graph.nodes()))
print(nodes_json)
```

## Complete Example

```python
#!/usr/bin/env python3
"""Analyze a graph and find important nodes."""

from gfx.parser import GEXFGraph, GEXFParseError
from collections import Counter

def analyze_connectivity(filepath: str) -> None:
    """Find the most connected nodes in a graph."""
    try:
        graph = GEXFGraph(filepath)
    except GEXFParseError as e:
        print(f"Error: {e}")
        return

    print(f"Analyzing: {filepath}")
    print(f"  Nodes: {graph.metadata.node_count}")
    print(f"  Edges: {graph.metadata.edge_count}")
    print()

    # Count outgoing edges per node
    edges = list(graph.edges())
    out_degree = Counter(e.source for e in edges)
    in_degree = Counter(e.target for e in edges)

    # Find hub nodes (high out-degree)
    print("Top 5 Hub Nodes (outgoing edges):")
    for node_id, count in out_degree.most_common(5):
        node = graph.get_node(node_id)
        label = node.label if node else node_id
        print(f"  {label}: {count} outgoing edges")

    print()

    # Find authority nodes (high in-degree)
    print("Top 5 Authority Nodes (incoming edges):")
    for node_id, count in in_degree.most_common(5):
        node = graph.get_node(node_id)
        label = node.label if node else node_id
        print(f"  {label}: {count} incoming edges")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file.gexf>")
        sys.exit(1)
    analyze_connectivity(sys.argv[1])
```

## Type Hints

All public APIs are fully typed:

```python
from gfx.parser import GEXFGraph
from gfx.models import Node, Edge, GraphMetadata
from typing import Iterator

def process_servers(graph: GEXFGraph) -> list[Node]:
    """Get all server nodes."""
    servers: Iterator[Node] = graph.nodes(attr_filters=[("type", "server")])
    return list(servers)
```
