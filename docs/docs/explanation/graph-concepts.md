---
sidebar_position: 2
title: Graph Concepts
---

# Graph Concepts

This article explains the fundamental concepts you need to understand when working with graphs. Even if you're familiar with graphs, reviewing these concepts helps you get the most out of grph.

## What is a Graph?

A **graph** is a collection of **nodes** (also called vertices) connected by **edges** (also called links or relationships). Graphs represent relationships between things.

```
   A ───── B
   │       │
   │       │
   C ───── D
```

In this simple graph:
- **Nodes**: A, B, C, D
- **Edges**: A-B, A-C, B-D, C-D

## Directed vs Undirected Graphs

### Undirected Graphs

In an undirected graph, edges have no direction. If A connects to B, then B connects to A.

**Examples:**
- **London Underground**: You can travel in either direction between stations
- **Facebook friendships**: If you're friends with someone, they're friends with you
- **Physical networks**: Roads (usually), cables, pipes

```
   A ───── B    (A connects to B, B connects to A)
```

In grph:
```bash
grph neighbors graph.gexf nodeA
# Shows all connected nodes, regardless of direction
```

### Directed Graphs

In a directed graph, edges have direction. A → B doesn't mean B → A.

**Examples:**
- **Flight routes**: A flight from London to Barcelona doesn't imply a return flight
- **Twitter follows**: You can follow someone who doesn't follow you back
- **Dependencies**: Package A depends on B, but B doesn't depend on A

```
   A ────→ B    (A points to B, but B doesn't point to A)
```

In grph, direction matters:
```bash
# What can I reach FROM this node?
grph neighbors graph.gexf nodeA --direction out

# What nodes point TO this node?
grph neighbors graph.gexf nodeA --direction in
```

## Weighted vs Unweighted Graphs

### Unweighted Graphs

All edges are equal. The only question is: are two nodes connected or not?

**Example:** Social network follows - you either follow someone or you don't.

### Weighted Graphs

Edges have values (weights) representing strength, distance, or cost.

**Examples:**
- **Transport networks**: Edge weight = travel time or distance
- **Social networks**: Edge weight = interaction strength
- **Dependencies**: Edge weight = frequency of use

```
   A ──5── B    (Edge has weight 5, perhaps 5 minutes travel time)
   │       │
   2       3
   │       │
   C ──4── D
```

Weights affect path finding - the "shortest" path minimizes total weight, not edge count.

## Paths and Connectivity

### Path

A **path** is a sequence of nodes where each consecutive pair is connected by an edge.

```
Path from A to D: A → B → D
```

### Shortest Path

The path with the minimum number of edges (unweighted) or minimum total weight (weighted).

### Connected Graph

A graph where every node can reach every other node through some path.

### Strongly Connected (Directed Graphs)

A directed graph where you can get from any node to any other node following edge directions.

## Components

### Connected Components (Undirected)

Groups of nodes that are connected to each other but not to nodes in other groups.

```
Component 1:    Component 2:
   A ─── B         E ─── F
   │               │
   C               G
```

### Strongly Connected Components (Directed)

Groups where every node can reach every other node in the group, following edge directions. These indicate cycles.

## Why These Concepts Matter

Understanding these concepts helps you:

1. **Choose the right analysis**: Use `--direction in` or `out` for directed graphs
2. **Interpret results correctly**: A path existing A→B doesn't mean B→A in directed graphs
3. **Select appropriate metrics**: Some centrality measures only make sense for directed graphs
4. **Identify the right questions**: Components analysis differs for directed vs undirected

## In grph

Check your graph's type:

```bash
grph info graph.gexf
```

Look at "Default Edge Type" to see if your graph is directed or undirected.
