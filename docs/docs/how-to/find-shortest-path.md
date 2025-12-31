---
sidebar_position: 2
title: Find the Shortest Path
---

# How to Find the Shortest Path

Find the shortest path between two nodes in your graph.

## Quick Answer

```bash
grph path graph.gexf source-node target-node
```

## Examples

### Basic Path Finding

```bash
# Find route between two stations
grph path london-underground.gexf kings-cross bank

# Output:
# Path from kings-cross to bank
# Length: 4 edges
# Path: kings-cross → russell-square → holborn → chancery-lane → bank
```

### Check If Path Exists First

```bash
# Check if connected
grph has-path graph.gexf nodeA nodeB

# Output: Path exists: Yes/No
```

### Find Path in Directed Graph

For directed graphs, direction matters:

```bash
# Can we get FROM A TO B?
grph path flights.gexf LTN DBV

# This might fail even if the reverse path exists
grph path flights.gexf DBV LTN
```

## Related

- [Find All Possible Routes](./find-all-routes) - When you need alternatives
- `grph path --help` - Full command documentation
