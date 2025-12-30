---
sidebar_position: 2
title: JSON Output
---

# Working with JSON Output

All GFX CLI commands support the `--json` flag for machine-readable output. This page covers how to use JSON output effectively.

## Basic JSON Output

Add `--json` to any command:

```bash
gfx info graph.gexf --json
gfx meta graph.gexf --json
gfx nodes graph.gexf --json
gfx edges graph.gexf --json
```

## Output Formats

### Info Command

```bash
gfx info graph.gexf --json
```

```json
{
  "file": "graph.gexf",
  "version": "1.2",
  "mode": "static",
  "default_edge_type": "directed",
  "node_count": 5,
  "edge_count": 6,
  "node_attributes": ["type", "weight"],
  "edge_attributes": ["relationship"]
}
```

### Meta Command

```bash
gfx meta graph.gexf --json
```

```json
{
  "creator": "Gephi 0.10.1",
  "description": "Sample network",
  "last_modified": "2024-01-15",
  "mode": "static",
  "default_edge_type": "directed",
  "version": "1.2",
  "node_count": 5,
  "edge_count": 6
}
```

### Nodes Command

```bash
gfx nodes graph.gexf --json
```

```json
[
  {
    "id": "server1",
    "label": "Web Server 1",
    "attributes": {
      "type": "server",
      "weight": 1.5
    }
  },
  {
    "id": "server2",
    "label": "Web Server 2",
    "attributes": {
      "type": "server",
      "weight": 2.0
    }
  }
]
```

### Edges Command

```bash
gfx edges graph.gexf --json
```

```json
[
  {
    "id": "e0",
    "source": "lb1",
    "target": "server1",
    "weight": 1.0,
    "type": null,
    "label": null,
    "attributes": {
      "relationship": "routes"
    }
  }
]
```

## Using with jq

[jq](https://jqlang.github.io/jq/) is a powerful command-line JSON processor. Here are common patterns:

### Extract Specific Fields

```bash
# Get just node IDs
gfx nodes graph.gexf --json | jq '.[].id'

# Get IDs and labels
gfx nodes graph.gexf --json | jq '.[] | {id, label}'
```

### Filtering

```bash
# Nodes with weight > 1.0
gfx nodes graph.gexf --json | jq '[.[] | select(.attributes.weight > 1.0)]'

# Edges with non-null weight
gfx edges graph.gexf --json | jq '[.[] | select(.weight != null)]'
```

### Counting

```bash
# Count nodes by type
gfx nodes graph.gexf --json | jq 'group_by(.attributes.type) | map({type: .[0].attributes.type, count: length})'
```

### Unique Values

```bash
# Get unique node types
gfx nodes graph.gexf --json | jq '[.[].attributes.type] | unique'

# Get unique edge relationships
gfx edges graph.gexf --json | jq '[.[].attributes.relationship] | unique'
```

### Transforming

```bash
# Create a simple adjacency list
gfx edges graph.gexf --json | jq 'group_by(.source) | map({node: .[0].source, targets: [.[].target]})'
```

## Piping to Other Tools

### Python Processing

```bash
gfx nodes graph.gexf --json | python3 -c "
import json, sys
nodes = json.load(sys.stdin)
for node in nodes:
    if node['attributes'].get('weight', 0) > 1.0:
        print(f\"{node['id']}: {node['label']}\")
"
```

### Save to File

```bash
gfx nodes graph.gexf --json > nodes.json
gfx edges graph.gexf --json > edges.json
```

### Convert to CSV

```bash
# Nodes to CSV
gfx nodes graph.gexf --json | jq -r '["id","label","type"], (.[] | [.id, .label, .attributes.type]) | @csv'

# Edges to CSV
gfx edges graph.gexf --json | jq -r '["source","target","weight"], (.[] | [.source, .target, .weight]) | @csv'
```

## Combining Commands

### Compare Two Graphs

```bash
# Find nodes in graph1 but not in graph2
comm -23 \
  <(gfx nodes graph1.gexf --json | jq -r '.[].id' | sort) \
  <(gfx nodes graph2.gexf --json | jq -r '.[].id' | sort)
```

### Build a Report

```bash
echo "Graph Report"
echo "============"
echo ""
echo "Summary:"
gfx info graph.gexf --json | jq -r '"  Nodes: \(.node_count)\n  Edges: \(.edge_count)"'
echo ""
echo "Node Types:"
gfx nodes graph.gexf --json | jq -r 'group_by(.attributes.type) | .[] | "  \(.[0].attributes.type): \(length)"'
```

## Error Handling

When a file is invalid or not found, GFX CLI exits with code 1:

```bash
gfx info nonexistent.gexf --json
# Exit code: 1
# Output: Error: File not found: nonexistent.gexf
```

Check for errors in scripts:

```bash
if output=$(gfx nodes graph.gexf --json 2>&1); then
    echo "$output" | jq '.'
else
    echo "Error: $output"
    exit 1
fi
```
