---
sidebar_position: 8
title: Extract Subgraphs
---

# How to Extract Subgraphs

Create focused views of your graph by extracting specific nodes and their connections.

## Quick Answer

```bash
# Extract specific nodes
grph subgraph graph.gexf node1 node2 node3 --output subset.gexf

# Extract neighborhood around a node
grph ego graph.gexf central-node --radius 2 --output neighborhood.gexf
```

## Methods

### Method 1: Ego Network (Neighborhood)

Extract a node and everything within N steps:

```bash
# Get @codequeen and everyone 1 step away
grph ego social.gexf codequeen --radius 1

# Get Oxford Circus and everything within 2 stops
grph ego underground.gexf oxford-circus --radius 2
```

### Method 2: Specific Nodes

Extract exactly the nodes you specify:

```bash
# Extract just UK airports
grph subgraph flights.gexf LTN LGW STN BRS EDI MAN BFS
```

### Method 3: Based on Path

Extract nodes along a path:

```bash
# First find the path
grph path graph.gexf A B

# Then extract those nodes manually
grph subgraph graph.gexf A intermediate1 intermediate2 B
```

## Saving Subgraphs

Add `--output` to save:

```bash
grph ego graph.gexf central --radius 2 --output focused.gexf
```

## Use Cases

- **Reduce complexity**: Focus on relevant parts of large graphs
- **Visualization**: Create manageable views for diagrams
- **Analysis**: Study local structure without noise

## Related

- [Export for Visualization](./export-for-visualization) - Export the subgraph
- [Filter Nodes by Attributes](./filter-by-attributes) - Another way to focus
