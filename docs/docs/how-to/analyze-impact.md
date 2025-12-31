---
sidebar_position: 9
title: Analyze Impact
---

# How to Analyze Impact of Changes

Understand what's affected when a node changes, fails, or is removed.

## Quick Answer

```bash
# What depends on this node? (incoming edges)
grph neighbors graph.gexf target-node --direction in

# What does this node depend on? (outgoing edges)
grph neighbors graph.gexf target-node --direction out
```

## Examples

### Dependency Impact Analysis

If we upgrade React, what packages are affected?

```bash
# Find all packages that depend on React
grph neighbors dependencies.gexf react --direction in
```

### Transitive Impact

What about packages that depend on packages that depend on React?

```bash
# Expand to depth 2
grph neighbors dependencies.gexf react --direction in --depth 2
```

### Service Impact Analysis

If auth-service goes down, what breaks?

```bash
# Find all services that call auth-service
grph neighbors microservices.gexf auth-service --direction in --depth 3
```

### Network Failure Analysis

If a critical router fails, what's affected?

```bash
# Find everything reachable from/through this node
grph neighbors network.gexf critical-router --depth 2
```

## Quantifying Impact

Count affected nodes:

```bash
grph neighbors graph.gexf node --direction in --json | grep '"id"' | wc -l
```

## Identify Critical Nodes

Nodes with high betweenness are critical - many paths go through them:

```bash
grph centrality graph.gexf --type betweenness --top 10
```

These nodes cause the most disruption if removed.

## Related

- [Detect Circular Dependencies](./detect-circular-dependencies) - Find cycles
- [Find Bridge Nodes](./find-bridge-nodes) - Find critical connectors
