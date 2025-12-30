---
sidebar_position: 2
title: grph info
---

# grph info

Display a summary of the graph including node/edge counts and available attributes.

## Synopsis

```bash
grph info <file> [--json]
```

## Description

The `info` command provides a quick overview of a GEXF graph file. It displays:

- File path
- GEXF version
- Graph mode (static/dynamic)
- Default edge type (directed/undirected)
- Total node count
- Total edge count
- Available node attributes
- Available edge attributes

This is useful for quickly understanding the structure of an unfamiliar graph file.

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |

## Options

| Option | Description |
|--------|-------------|
| `--json` | Output as JSON instead of a table |
| `--help` | Show help message |

## Examples

### Basic Usage

```bash
grph info network.gexf
```

Output:
```
                  Graph Summary
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Property          ┃ Value                      ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ File              │ network.gexf               │
│ Version           │ 1.2                        │
│ Mode              │ static                     │
│ Default Edge Type │ directed                   │
│ Node Count        │ 150                        │
│ Edge Count        │ 420                        │
└───────────────────┴────────────────────────────┘

Node Attributes: type, weight, category
Edge Attributes: relationship, strength
```

### JSON Output

```bash
grph info network.gexf --json
```

```json
{
  "file": "network.gexf",
  "version": "1.2",
  "mode": "static",
  "default_edge_type": "directed",
  "node_count": 150,
  "edge_count": 420,
  "node_attributes": ["category", "type", "weight"],
  "edge_attributes": ["relationship", "strength"]
}
```

## Use Cases

### Quick Inspection

Before working with a new graph file, use `info` to understand its structure:

```bash
grph info unknown-graph.gexf
```

### Scripting

Check if a graph has certain attributes before processing:

```bash
if grph info graph.gexf --json | jq -e '.node_attributes | contains(["type"])' > /dev/null; then
  echo "Graph has 'type' attribute on nodes"
fi
```

### Validation

Verify a graph file is valid and get basic stats:

```bash
grph info graph.gexf && echo "File is valid"
```
