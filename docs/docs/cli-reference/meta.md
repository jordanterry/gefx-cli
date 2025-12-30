---
sidebar_position: 3
title: grph meta
---

# grph meta

Display detailed metadata from a GEXF file.

## Synopsis

```bash
grph meta <file> [--json]
```

## Description

The `meta` command extracts and displays the metadata section of a GEXF file. This includes information stored in the `<meta>` element of the GEXF XML:

- **Creator** - The tool or person who created the file
- **Description** - A description of the graph
- **Last Modified** - When the file was last modified
- **Version** - The GEXF format version
- **Mode** - Static or dynamic graph
- **Default Edge Type** - Directed or undirected

This is useful for understanding the provenance and purpose of a graph file.

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |

## Options

| Option | Description |
|--------|-------------|
| `--json` | Output as JSON instead of a table |
| `--help` | Show help message |

## Examples

### Basic Usage

```bash
grph meta social-network.gexf
```

Output:
```
                          Graph Metadata
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Property          ┃ Value                                       ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Version           │ 1.2                                         │
│ Creator           │ Gephi 0.10.1                                │
│ Description       │ Social network of software developers       │
│ Last Modified     │ 2024-01-15                                  │
│ Mode              │ static                                      │
│ Default Edge Type │ undirected                                  │
│ Node Count        │ 1250                                        │
│ Edge Count        │ 8420                                        │
└───────────────────┴─────────────────────────────────────────────┘
```

### JSON Output

```bash
grph meta social-network.gexf --json
```

```json
{
  "creator": "Gephi 0.10.1",
  "description": "Social network of software developers",
  "last_modified": "2024-01-15",
  "mode": "static",
  "default_edge_type": "undirected",
  "version": "1.2",
  "node_count": 1250,
  "edge_count": 8420
}
```

## Difference from `grph info`

| Command | Purpose |
|---------|---------|
| `grph info` | Quick summary + available attributes list |
| `grph meta` | Full metadata (creator, description, dates) |

Use `info` for a quick overview including attribute names. Use `meta` when you need the full metadata including who created the file and when.

## Missing Metadata

If metadata fields are not present in the GEXF file, they will show as "N/A":

```
┃ Creator           ┃ N/A                                         ┃
┃ Description       ┃ N/A                                         ┃
```

Not all GEXF files include metadata. The `<meta>` element is optional in the GEXF specification.
