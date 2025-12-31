---
sidebar_position: 3
title: Centrality Metrics Explained
---

# Centrality Metrics Explained

Centrality metrics measure how "important" a node is in a graph. But "important" can mean different things. This article explains each metric and when to use it.

## Overview

| Metric | Question It Answers | Good For |
|--------|---------------------|----------|
| **Degree** | How many connections? | Finding popular nodes |
| **Betweenness** | How many paths go through? | Finding bridges/bottlenecks |
| **Closeness** | How quickly can it reach others? | Finding efficient spreaders |
| **PageRank** | How important are its connections? | Finding true influence |
| **Eigenvector** | How connected to well-connected? | Finding inner circle |

## Degree Centrality

**Question:** How many direct connections does this node have?

**Calculation:** Count of edges connected to the node, normalized by the maximum possible.

**Interpretation:**
- High degree = many direct connections
- In social networks: popular accounts
- In transport: hub stations
- In dependencies: commonly used packages

**For Directed Graphs:**
- **In-degree**: How many edges point TO this node (followers, dependents)
- **Out-degree**: How many edges point FROM this node (following, dependencies)

```bash
grph centrality graph.gexf --type degree
grph degree graph.gexf --direction in   # For directed: incoming
grph degree graph.gexf --direction out  # For directed: outgoing
```

**When to use:** Quick measure of popularity or connectivity.

**Limitation:** Doesn't consider the quality of connections. A node with 100 low-quality connections scores higher than one with 10 high-quality connections.

## Betweenness Centrality

**Question:** How often does this node appear on the shortest path between other nodes?

**Calculation:** For each pair of nodes, find all shortest paths. Count what fraction pass through this node.

**Interpretation:**
- High betweenness = bridge position
- Controls information flow between parts of the network
- Critical for network connectivity
- Removing it would increase average path length

**Examples:**
- **Transport**: Stations where many routes converge
- **Social**: People who connect different groups
- **Infrastructure**: Routers handling traffic between networks

```bash
grph centrality graph.gexf --type betweenness
```

**When to use:** Finding bottlenecks, single points of failure, or critical connectors.

**Limitation:** Computationally expensive for large graphs.

## Closeness Centrality

**Question:** How quickly can this node reach all other nodes?

**Calculation:** Inverse of the average shortest path length to all other nodes.

**Interpretation:**
- High closeness = central position
- Can spread information quickly
- Low average distance to everyone else

**Examples:**
- **Epidemiology**: Who can spread disease most efficiently?
- **Information**: Who can reach everyone with fewest hops?
- **Logistics**: Best location for a distribution center

```bash
grph centrality graph.gexf --type closeness
```

**When to use:** Finding efficient starting points for spreading information or influence.

**Limitation:** Only works well for connected graphs. Disconnected graphs have infinite distances.

## PageRank

**Question:** How important is this node, considering the importance of nodes that connect to it?

**Calculation:** Iterative algorithm originally designed by Google. A node is important if important nodes link to it.

**Interpretation:**
- High PageRank = endorsed by important nodes
- Quality over quantity
- Being followed by an influencer matters more than being followed by many nobodies

**Examples:**
- **Web**: Pages linked by authoritative sites rank higher
- **Social**: Users followed by influencers are more influential
- **Citations**: Papers cited by landmark papers are more significant

```bash
grph centrality graph.gexf --type pagerank
```

**When to use:** Finding true influence or authority, especially in directed networks.

**Key insight:** Unlike degree, PageRank considers WHO links to you, not just how many.

## Eigenvector Centrality

**Question:** How well-connected is this node to other well-connected nodes?

**Calculation:** Based on the graph's adjacency matrix eigenvalues. A node is important if its neighbors are important.

**Interpretation:**
- Similar to PageRank but symmetric
- Measures being "in the club"
- High score means connected to the well-connected

**Examples:**
- **Social**: Part of an influential inner circle
- **Collaboration**: Works with productive researchers
- **Business**: Connected to powerful organizations

```bash
grph centrality graph.gexf --type eigenvector
```

**When to use:** Finding nodes embedded in influential clusters.

**Limitation:** Can be unstable for directed graphs. Use PageRank for directed networks.

## Choosing the Right Metric

### For Social Networks
1. **PageRank** - True influence (who has influential followers?)
2. **In-degree** - Raw popularity (who has the most followers?)
3. **Betweenness** - Connectors (who bridges different communities?)

### For Infrastructure/Transport
1. **Betweenness** - Critical nodes (which stations/routers are bottlenecks?)
2. **Degree** - Hub nodes (which have most connections?)
3. **Closeness** - Efficiency (which can reach everywhere quickly?)

### For Dependencies
1. **In-degree** - Most depended upon (what do most packages use?)
2. **Betweenness** - Critical path (what's in most dependency chains?)
3. **PageRank** - Core importance (what do the important packages depend on?)

## Comparing Metrics

Different metrics highlight different things:

```bash
# Run multiple metrics on the same graph
grph centrality graph.gexf --type degree --top 5
grph centrality graph.gexf --type betweenness --top 5
grph centrality graph.gexf --type pagerank --top 5
```

When the same nodes appear across metrics, they're genuinely central. When different nodes appear, each metric is capturing a different type of importance.

## Summary

| Want to find... | Use... |
|-----------------|--------|
| Most connected | Degree |
| Bottlenecks | Betweenness |
| Best spreaders | Closeness |
| True influencers | PageRank |
| Inner circle | Eigenvector |
