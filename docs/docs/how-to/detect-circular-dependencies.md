---
sidebar_position: 5
title: Detect Circular Dependencies
---

# How to Detect Circular Dependencies

Find cycles in directed graphs like dependency trees, build systems, or module imports.

## Quick Answer

```bash
# Find strongly connected components (cycles)
grph components graph.gexf --type strongly --list
```

Any strongly connected component with more than one node indicates a cycle.

## Understanding the Output

```bash
grph components dependencies.gexf --type strongly

# Output:
# Strongly Connected Components
# ┃ Statistic       ┃ Value ┃
# ├─────────────────┼───────┤
# │ Total           │ 35    │
# │ Largest         │ 3     │  ← A cycle of 3 nodes!
```

If "Largest" is greater than 1, you have circular dependencies.

## Find the Actual Cycles

List all components to find which nodes are in cycles:

```bash
grph components dependencies.gexf --type strongly --list
```

Look for components with multiple nodes - these are your cycles.

## Example: Finding Dependency Cycles

```bash
# Check if module A and B have a cycle
grph has-path deps.gexf A B
grph has-path deps.gexf B A

# If both return Yes, you have a cycle
```

## Why Cycles Matter

- **Build systems**: Cycles prevent proper build ordering
- **Module imports**: Cycles can cause import errors
- **Dependencies**: Cycles create version resolution issues

## Related

- [Analyze Impact](./analyze-impact) - Understand dependency effects
- `grph components --help` - Full command documentation
