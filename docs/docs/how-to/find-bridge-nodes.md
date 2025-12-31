---
sidebar_position: 10
title: Find Bridge Nodes
---

# How to Find Bridge Nodes

Identify nodes that are critical for connectivity - their removal would disconnect parts of the network.

## Quick Answer

```bash
grph centrality graph.gexf --type betweenness --top 10
```

Nodes with high betweenness centrality are bridge nodes.

## Understanding Bridge Nodes

A bridge node lies on many shortest paths between other nodes. If removed:
- Communication between parts of the network is disrupted
- Average path length increases
- Some nodes may become unreachable

## Examples

### Find Network Bottlenecks

```bash
grph centrality network.gexf --type betweenness --top 5
```

These are your single points of failure.

### Find Social Connectors

```bash
grph centrality social.gexf --type betweenness --top 5
```

These people connect different communities.

### Find Critical Transit Points

```bash
grph centrality underground.gexf --type betweenness --top 5
```

Stations that connect different parts of the network.

## Verifying Bridge Status

Check what happens if a suspected bridge is "removed":

```bash
# Extract the network without the bridge node
grph subgraph graph.gexf node1 node2 node3 ...  # exclude the bridge

# Check if still connected
grph stats subset.gexf  # Look at "Connected" status
```

## Related

- [Find Influencers](./find-influencers) - Other centrality measures
- [Analyze Impact](./analyze-impact) - Impact of node changes
- [Centrality Metrics Explained](../explanation/centrality-metrics) - Understanding metrics
