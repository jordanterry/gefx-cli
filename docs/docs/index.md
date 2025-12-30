---
sidebar_position: 1
slug: /
title: Introduction
---

# grph CLI

A powerful command-line tool for interrogating and browsing **GEXF** (Graph Exchange XML Format) graph files.

## What is grph CLI?

grph CLI (`grph`) is a Python-based command-line tool that allows you to:

- **Inspect graph metadata** - View creator, description, modification dates, and graph properties
- **Browse nodes** - List all nodes or filter by attributes and label patterns
- **Browse edges** - List all edges or filter by source, target, type, and attributes
- **Export to JSON** - Get machine-readable output for scripting and automation

## Why grph CLI?

Working with GEXF files typically requires loading them into a graph visualization tool like Gephi. But sometimes you just need to quickly:

- Check how many nodes and edges are in a graph
- Find all nodes of a certain type
- Extract edges connecting specific nodes
- Pipe graph data into other tools

grph CLI makes these tasks fast and scriptable from your terminal.

## Quick Example

```bash
# Get a quick overview of a graph
$ grph info network.gexf

# Find all nodes with type="server"
$ grph nodes network.gexf --attr type=server

# Get edges from a specific node as JSON
$ grph edges network.gexf --source node1 --json
```

## Features

| Feature | Description |
|---------|-------------|
| **Rich Tables** | Beautiful terminal output with automatic column sizing |
| **JSON Output** | Machine-readable output with `--json` flag |
| **Flexible Filtering** | Filter by attributes, labels, source/target nodes |
| **AND Logic** | Multiple filters are combined with AND logic |
| **Pattern Matching** | Use wildcards (`*`, `?`) in label filters |

## Installation

```bash
pip install gfx-cli
```

Or install from source:

```bash
git clone https://github.com/your-username/gfx-cli.git
cd gfx-cli
pip install -e .
```

## Next Steps

- [Getting Started](./getting-started) - Installation and first commands
- [CLI Reference](./cli-reference/) - Complete command documentation
- [GEXF Format](./gexf-format) - Understanding the GEXF file format
- [Examples](./examples/filtering) - Real-world usage examples
