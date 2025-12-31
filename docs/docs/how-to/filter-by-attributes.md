---
sidebar_position: 7
title: Filter Nodes by Attributes
---

# How to Filter Nodes by Attributes

Find specific nodes based on their properties.

## Quick Answer

```bash
grph nodes graph.gexf --attr key=value
```

## Examples

### Filter by Single Attribute

```bash
# Find all hub airports
grph nodes flights.gexf --attr hub=True

# Find verified users
grph nodes social.gexf --attr verified=True

# Find deprecated packages
grph nodes dependencies.gexf --attr deprecated=True
```

### Filter by Category/Type

```bash
# Find all server nodes
grph nodes network.gexf --attr type=server

# Find tech accounts
grph nodes social.gexf --attr category=tech
```

### Filter by Numeric Values

```bash
# Find nodes in zone 1
grph nodes underground.gexf --attr zone=1
```

### Filter by Label Pattern

Use `--label` for pattern matching:

```bash
# Find nodes with "test" in the label
grph nodes graph.gexf --label "test"

# Find @testing-library packages
grph nodes npm.gexf --label "@testing-library"
```

### Combine with JSON Output

```bash
# Get filtered results as JSON for further processing
grph nodes graph.gexf --attr type=server --json | jq '.[].id'
```

## Finding Available Attributes

First, see what attributes exist:

```bash
grph info graph.gexf
```

The output shows "Node Attributes" - use these with `--attr`.

## Related

- [Extract Subgraphs](./extract-subgraphs) - Create subgraphs from filtered nodes
- `grph nodes --help` - Full command documentation
