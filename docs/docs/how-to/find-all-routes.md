---
sidebar_position: 3
title: Find All Possible Routes
---

# How to Find All Possible Routes

Discover all paths between two nodes, not just the shortest one.

## Quick Answer

```bash
grph all-paths graph.gexf source target --max-depth 5
```

## Examples

### Find Alternative Routes

```bash
# Find all routes with up to 5 connections
grph all-paths london-underground.gexf oxford-circus bank --max-depth 5

# Output shows multiple paths
```

### Limit Results

For highly connected graphs, limit the output:

```bash
# Find first 10 paths
grph all-paths graph.gexf A B --max-depth 4 | head -20
```

### Export to JSON for Processing

```bash
grph all-paths graph.gexf A B --max-depth 4 --json > routes.json
```

## When to Use

- **Route optimization**: Find alternatives when the shortest isn't best
- **Redundancy analysis**: How many ways can you get from A to B?
- **Network resilience**: What happens if one path is blocked?

## Warning

All-paths can be computationally expensive on dense graphs. Use `--max-depth` to limit search depth.

## Related

- [Find the Shortest Path](./find-shortest-path) - When you just need one path
- `grph all-paths --help` - Full command documentation
