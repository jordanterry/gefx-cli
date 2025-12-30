---
sidebar_position: 4
title: grph nodes
---

# grph nodes

List and filter nodes in the graph.

## Synopsis

```bash
grph nodes <file> [--attr KEY=VALUE]... [--label PATTERN] [--json] [--no-attrs]
```

## Description

The `nodes` command lists all nodes in a GEXF graph, with optional filtering capabilities. You can filter nodes by:

- **Attribute values** - Match nodes with specific attribute values
- **Label patterns** - Match node labels using wildcard patterns

When multiple filters are specified, they are combined with **AND logic** - a node must match all filters to be included.

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |

## Options

| Option | Description |
|--------|-------------|
| `--attr KEY=VALUE` | Filter by attribute. Can be specified multiple times. |
| `--label PATTERN` | Filter by label pattern. Supports `*` and `?` wildcards. |
| `--json` | Output as JSON instead of a table |
| `--no-attrs` | Hide the attributes column in table output |
| `--help` | Show help message |

## Examples

### List All Nodes

```bash
grph nodes network.gexf
```

Output:
```
                        Nodes (5)
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID      ┃ Label            ┃ Attributes                    ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ server1 │ Web Server 1     │ type=server, weight=1.5       │
│ server2 │ Web Server 2     │ type=server, weight=2.0       │
│ db1     │ Database Primary │ type=database, weight=3.0     │
│ cache1  │ Redis Cache      │ type=cache, weight=1.0        │
│ lb1     │ Load Balancer    │ type=loadbalancer, weight=0.5 │
└─────────┴──────────────────┴───────────────────────────────┘
```

### Filter by Attribute

Find all server nodes:

```bash
grph nodes network.gexf --attr type=server
```

Output:
```
                     Nodes (2)
┏━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID      ┃ Label        ┃ Attributes              ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ server1 │ Web Server 1 │ type=server, weight=1.5 │
│ server2 │ Web Server 2 │ type=server, weight=2.0 │
└─────────┴──────────────┴─────────────────────────┘
```

### Filter by Label Pattern

Find nodes with labels starting with "Web":

```bash
grph nodes network.gexf --label "Web*"
```

### Multiple Filters (AND Logic)

Find server nodes with weight=2.0:

```bash
grph nodes network.gexf --attr type=server --attr weight=2.0
```

This returns only nodes where **both** conditions are true.

### JSON Output

```bash
grph nodes network.gexf --attr type=server --json
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

### Hide Attributes Column

For a cleaner view with just IDs and labels:

```bash
grph nodes network.gexf --no-attrs
```

```
           Nodes (5)
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ ID      ┃ Label            ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ server1 │ Web Server 1     │
│ server2 │ Web Server 2     │
│ db1     │ Database Primary │
│ cache1  │ Redis Cache      │
│ lb1     │ Load Balancer    │
└─────────┴──────────────────┘
```

## Label Pattern Syntax

The `--label` option supports glob-style patterns:

| Pattern | Matches |
|---------|---------|
| `*` | Any sequence of characters |
| `?` | Any single character |
| `[abc]` | Any character in brackets |
| `[!abc]` | Any character not in brackets |

Examples:
- `--label "Web*"` - Labels starting with "Web"
- `--label "*Server*"` - Labels containing "Server"
- `--label "Node?"` - "Node" followed by any single character
- `--label "Server[12]"` - "Server1" or "Server2"

## Attribute Value Matching

Attribute values are compared as strings. This means:

- `--attr weight=1.5` matches the string "1.5"
- Numeric comparisons (`>`, `<`) are not supported
- Matching is case-sensitive

For complex filtering, use `--json` and pipe to `jq`:

```bash
grph nodes graph.gexf --json | jq '[.[] | select(.attributes.weight > 1.0)]'
```
