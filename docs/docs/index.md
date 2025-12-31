---
sidebar_position: 1
slug: /
title: Introduction
---

# grph

> Like grep, but for graphs.

A powerful command-line tool for exploring, analyzing, and querying graph files. Built for developers, data scientists, and anyone who works with graph data.

## What is grph?

grph is a Python-based CLI tool that lets you explore and analyze graph files from your terminal. Think of it as `grep` for graphs - quick answers to graph questions without leaving the command line.

### Core Capabilities

- **Graph Traversal** - Find neighbors, paths, and reachable nodes
- **Graph Analysis** - Calculate centrality, find components, get statistics
- **Filtering** - Find nodes and edges by attributes
- **Export** - Output to JSON, GraphML, and other formats

## Quick Examples

```bash
# Get an overview of your graph
grph info network.gexf

# Find the shortest path between two nodes
grph path network.gexf server1 database

# Find the most influential nodes
grph centrality social-network.gexf --type pagerank --top 10

# What depends on this package?
grph neighbors dependencies.gexf lodash --direction in

# Export for visualization
grph export network.gexf --format json --output network.json
```

## Features

| Category | Commands |
|----------|----------|
| **Basic** | `info`, `meta`, `nodes`, `edges` |
| **Traversal** | `neighbors`, `path`, `all-paths`, `has-path`, `reachable`, `common-neighbors` |
| **Analysis** | `stats`, `centrality`, `components`, `degree` |
| **Subgraphs** | `ego`, `subgraph` |
| **Export** | `export` (JSON, GraphML, adjacency list, edge list) |

## Installation

```bash
# Via pip
pip install grph-cli

# Via Homebrew (macOS)
brew tap jordanterry/grph https://github.com/jordanterry/grph
brew install grph-cli
```

## Documentation Structure

This documentation follows the [Divio documentation system](https://docs.divio.com/documentation-system/):

### [Tutorials](./tutorials/)
**Learning-oriented** step-by-step lessons. Start here if you're new to grph.

- [Exploring the London Underground](./tutorials/london-underground) - Beginner
- [Routing EasyJet Crew](./tutorials/easyjet-routing) - Intermediate
- [Analyzing npm Dependencies](./tutorials/npm-dependencies) - Intermediate
- [Finding Social Network Influencers](./tutorials/social-network) - Advanced

### [How-to Guides](./how-to/)
**Problem-oriented** recipes for specific tasks.

- [Find the Shortest Path](./how-to/find-shortest-path)
- [Detect Circular Dependencies](./how-to/detect-circular-dependencies)
- [Export for Visualization](./how-to/export-for-visualization)

### [Explanation](./explanation/)
**Understanding-oriented** discussions of concepts.

- [Graph Concepts](./explanation/graph-concepts)
- [Centrality Metrics Explained](./explanation/centrality-metrics)
- [When to Use grph](./explanation/when-to-use-grph)

### [CLI Reference](./cli-reference/)
**Information-oriented** technical reference for all commands.

## Next Steps

New to grph? Start with the [Getting Started](./getting-started) guide, then try the [London Underground tutorial](./tutorials/london-underground).

Have a specific problem? Check the [How-to Guides](./how-to/).

Need command details? See the [CLI Reference](./cli-reference/).
