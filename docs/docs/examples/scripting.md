---
sidebar_position: 3
title: Scripting
---

# Scripting with GFX CLI

GFX CLI is designed to work well in scripts and automation pipelines. This page covers common scripting patterns.

## Basic Scripting

### Exit Codes

GFX CLI uses standard exit codes:

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Error (file not found, parse error, etc.) |

```bash
if gfx info graph.gexf > /dev/null 2>&1; then
    echo "Valid GEXF file"
else
    echo "Invalid or missing file"
    exit 1
fi
```

### Capturing Output

```bash
# Capture JSON output
nodes=$(gfx nodes graph.gexf --json)
echo "Found $(echo "$nodes" | jq length) nodes"

# Capture specific values
node_count=$(gfx info graph.gexf --json | jq '.node_count')
echo "Graph has $node_count nodes"
```

## Shell Scripts

### Validate Multiple Files

```bash
#!/bin/bash
# validate-graphs.sh

for file in graphs/*.gexf; do
    if gfx info "$file" > /dev/null 2>&1; then
        echo "✓ $file"
    else
        echo "✗ $file (invalid)"
    fi
done
```

### Generate a Report

```bash
#!/bin/bash
# graph-report.sh

file="$1"

if [ -z "$file" ]; then
    echo "Usage: $0 <file.gexf>"
    exit 1
fi

echo "# Graph Report: $file"
echo ""

# Basic info
echo "## Summary"
gfx info "$file" --json | jq -r '"- Nodes: \(.node_count)\n- Edges: \(.edge_count)\n- Mode: \(.mode)"'
echo ""

# Node breakdown
echo "## Nodes by Type"
gfx nodes "$file" --json | jq -r 'group_by(.attributes.type) | .[] | "- \(.[0].attributes.type // "unknown"): \(length)"'
echo ""

# Top connected nodes
echo "## Most Connected Nodes (Outgoing)"
gfx edges "$file" --json | jq -r 'group_by(.source) | sort_by(-length) | .[0:5] | .[] | "- \(.[0].source): \(length) edges"'
```

### Find and Process

```bash
#!/bin/bash
# find-servers.sh

file="$1"

# Get all server nodes
servers=$(gfx nodes "$file" --attr type=server --json)

# Process each server
echo "$servers" | jq -c '.[]' | while read -r node; do
    id=$(echo "$node" | jq -r '.id')
    label=$(echo "$node" | jq -r '.label')

    # Count connections
    outgoing=$(gfx edges "$file" --source "$id" --json | jq 'length')
    incoming=$(gfx edges "$file" --target "$id" --json | jq 'length')

    echo "$label ($id): $outgoing outgoing, $incoming incoming"
done
```

## Python Integration

### Basic Usage

```python
import subprocess
import json

def get_graph_info(filepath):
    """Get graph info as a dictionary."""
    result = subprocess.run(
        ['gfx', 'info', filepath, '--json'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to read graph: {result.stderr}")
    return json.loads(result.stdout)

def get_nodes(filepath, **filters):
    """Get nodes with optional filters."""
    cmd = ['gfx', 'nodes', filepath, '--json']
    for key, value in filters.items():
        if key == 'label':
            cmd.extend(['--label', value])
        elif key == 'attr':
            for k, v in value.items():
                cmd.extend(['--attr', f'{k}={v}'])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get nodes: {result.stderr}")
    return json.loads(result.stdout)

# Usage
info = get_graph_info('network.gexf')
print(f"Graph has {info['node_count']} nodes")

servers = get_nodes('network.gexf', attr={'type': 'server'})
for server in servers:
    print(f"Server: {server['label']}")
```

### Analysis Script

```python
#!/usr/bin/env python3
"""Analyze a GEXF graph file."""

import subprocess
import json
import sys
from collections import Counter

def run_gfx(cmd):
    """Run a gfx command and return JSON output."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)

def analyze_graph(filepath):
    """Analyze a graph and print statistics."""
    info = run_gfx(['gfx', 'info', filepath, '--json'])
    nodes = run_gfx(['gfx', 'nodes', filepath, '--json'])
    edges = run_gfx(['gfx', 'edges', filepath, '--json'])

    print(f"Graph: {filepath}")
    print(f"  Nodes: {info['node_count']}")
    print(f"  Edges: {info['edge_count']}")
    print()

    # Node type distribution
    type_counts = Counter(n['attributes'].get('type', 'unknown') for n in nodes)
    print("Node Types:")
    for node_type, count in type_counts.most_common():
        print(f"  {node_type}: {count}")
    print()

    # Edge relationship distribution
    rel_counts = Counter(e['attributes'].get('relationship', 'unknown') for e in edges)
    print("Edge Relationships:")
    for rel, count in rel_counts.most_common():
        print(f"  {rel}: {count}")
    print()

    # Degree analysis
    out_degree = Counter(e['source'] for e in edges)
    in_degree = Counter(e['target'] for e in edges)

    print("Top 5 by Outgoing Edges:")
    for node_id, count in out_degree.most_common(5):
        node = next((n for n in nodes if n['id'] == node_id), None)
        label = node['label'] if node else node_id
        print(f"  {label}: {count}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file.gexf>")
        sys.exit(1)
    analyze_graph(sys.argv[1])
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Validate Graphs

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install gfx-cli
        run: pip install gfx-cli

      - name: Validate graph files
        run: |
          for file in data/*.gexf; do
            echo "Validating $file..."
            gfx info "$file"
          done
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Validate any GEXF files being committed
gexf_files=$(git diff --cached --name-only --diff-filter=ACM | grep '\.gexf$')

if [ -n "$gexf_files" ]; then
    echo "Validating GEXF files..."
    for file in $gexf_files; do
        if ! gfx info "$file" > /dev/null 2>&1; then
            echo "Error: Invalid GEXF file: $file"
            exit 1
        fi
        echo "  ✓ $file"
    done
fi
```

## Tips

### Performance

For large files, prefer filtered queries over fetching everything:

```bash
# Slower: fetch all, then filter
gfx nodes large.gexf --json | jq '[.[] | select(.attributes.type == "server")]'

# Faster: filter at source
gfx nodes large.gexf --attr type=server --json
```

### Error Messages

Redirect stderr to capture error messages separately:

```bash
output=$(gfx nodes graph.gexf --json 2>&1)
if [ $? -ne 0 ]; then
    echo "Error: $output"
fi
```

### Parallel Processing

Process multiple files in parallel:

```bash
# Using GNU parallel
find graphs/ -name "*.gexf" | parallel 'gfx info {} --json > {.}.info.json'

# Using xargs
find graphs/ -name "*.gexf" -print0 | xargs -0 -P4 -I{} sh -c 'gfx info "$1" --json' _ {}
```
