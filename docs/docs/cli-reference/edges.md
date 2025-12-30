---
sidebar_position: 5
title: gfx edges
---

# gfx edges

List and filter edges in the graph.

## Synopsis

```bash
gfx edges <file> [--attr KEY=VALUE]... [--source ID] [--target ID] [--type TYPE] [--json] [--no-attrs]
```

## Description

The `edges` command lists all edges in a GEXF graph, with optional filtering capabilities. You can filter edges by:

- **Attribute values** - Match edges with specific attribute values
- **Source node** - Match edges originating from a specific node
- **Target node** - Match edges pointing to a specific node
- **Edge type** - Match edges of a specific type (directed/undirected)

When multiple filters are specified, they are combined with **AND logic** - an edge must match all filters to be included.

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |

## Options

| Option | Description |
|--------|-------------|
| `--attr KEY=VALUE` | Filter by attribute. Can be specified multiple times. |
| `--source ID` | Filter by source node ID |
| `--target ID` | Filter by target node ID |
| `--type TYPE` | Filter by edge type (e.g., directed, undirected) |
| `--json` | Output as JSON instead of a table |
| `--no-attrs` | Hide the attributes column in table output |
| `--help` | Show help message |

## Examples

### List All Edges

```bash
gfx edges network.gexf
```

Output:
```
                           Edges (6)
┏━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Source ┃ Target  ┃ Weight ┃ Type ┃ Attributes          ┃
┡━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ e0 │ lb1    │ server1 │ 1.0    │      │ relationship=routes │
│ e1 │ lb1    │ server2 │ 1.0    │      │ relationship=routes │
│ e2 │ server1│ db1     │ 2.0    │      │ relationship=queries│
│ e3 │ server2│ db1     │ 2.0    │      │ relationship=queries│
│ e4 │ server1│ cache1  │ 0.5    │      │ relationship=caches │
│ e5 │ server2│ cache1  │ 0.5    │      │ relationship=caches │
└────┴────────┴─────────┴────────┴──────┴─────────────────────┘
```

### Filter by Source Node

Find all edges originating from the load balancer:

```bash
gfx edges network.gexf --source lb1
```

Output:
```
                           Edges (2)
┏━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Source ┃ Target  ┃ Weight ┃ Type ┃ Attributes          ┃
┡━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ e0 │ lb1    │ server1 │ 1.0    │      │ relationship=routes │
│ e1 │ lb1    │ server2 │ 1.0    │      │ relationship=routes │
└────┴────────┴─────────┴────────┴──────┴─────────────────────┘
```

### Filter by Target Node

Find all edges pointing to the database:

```bash
gfx edges network.gexf --target db1
```

### Filter by Attribute

Find all edges with a specific relationship:

```bash
gfx edges network.gexf --attr relationship=queries
```

### Combine Filters (AND Logic)

Find edges from server1 to db1:

```bash
gfx edges network.gexf --source server1 --target db1
```

Find query edges from server1:

```bash
gfx edges network.gexf --source server1 --attr relationship=queries
```

### JSON Output

```bash
gfx edges network.gexf --source lb1 --json
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
  },
  {
    "id": "e1",
    "source": "lb1",
    "target": "server2",
    "weight": 1.0,
    "type": null,
    "label": null,
    "attributes": {
      "relationship": "routes"
    }
  }
]
```

### Hide Attributes Column

```bash
gfx edges network.gexf --no-attrs
```

## Edge Properties

Each edge in the output includes:

| Property | Description |
|----------|-------------|
| **ID** | Unique edge identifier |
| **Source** | ID of the source node |
| **Target** | ID of the target node |
| **Weight** | Edge weight (if defined) |
| **Type** | Edge type (directed/undirected, if specified per-edge) |
| **Attributes** | Custom attributes defined in the GEXF file |

## Finding Connections

### All Edges for a Node

To find all edges connected to a node (both incoming and outgoing), run two queries:

```bash
# Outgoing edges
gfx edges graph.gexf --source nodeA

# Incoming edges
gfx edges graph.gexf --target nodeA
```

Or combine with JSON and jq:

```bash
gfx edges graph.gexf --json | jq '[.[] | select(.source == "nodeA" or .target == "nodeA")]'
```

### Path Between Nodes

To check if there's a direct edge between two nodes:

```bash
gfx edges graph.gexf --source nodeA --target nodeB
```

If no edges are returned, there's no direct connection.
