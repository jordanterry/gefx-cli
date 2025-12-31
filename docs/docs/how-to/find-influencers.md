---
sidebar_position: 4
title: Find Influencers
---

# How to Find Influential Nodes

Identify the most important, influential, or central nodes in your graph.

## Quick Answer

```bash
# Best general-purpose method
grph centrality graph.gexf --type pagerank --top 10
```

## Choose the Right Metric

| Metric | Use When | Command |
|--------|----------|---------|
| **PageRank** | Finding influential nodes (social, web) | `--type pagerank` |
| **Degree** | Finding most connected nodes | `--type degree` |
| **Betweenness** | Finding bridge/connector nodes | `--type betweenness` |
| **Closeness** | Finding nodes that can reach others quickly | `--type closeness` |
| **Eigenvector** | Finding nodes connected to important nodes | `--type eigenvector` |

## Examples

### Social Network Influencers

```bash
# Who has the most influential followers?
grph centrality social.gexf --type pagerank --top 5
```

### Network Hub Detection

```bash
# Which servers handle the most traffic?
grph centrality network.gexf --type degree --top 10
```

### Find Bottlenecks

```bash
# Which nodes are critical for connectivity?
grph centrality network.gexf --type betweenness --top 5
```

### For Directed Graphs

Specify direction for degree centrality:

```bash
# Most followed (incoming edges)
grph degree social.gexf --direction in --top 10

# Most following (outgoing edges)
grph degree social.gexf --direction out --top 10
```

## Related

- [Centrality Metrics Explained](../explanation/centrality-metrics) - Understand each metric
- [Find Bridge Nodes](./find-bridge-nodes) - Focus on connectors
