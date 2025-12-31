---
sidebar_position: 6
title: Export for Visualization
---

# How to Export Graphs for Visualization

Export your graph to formats compatible with visualization tools like D3.js, Gephi, or custom tools.

## Quick Answer

```bash
# For D3.js / web visualization
grph export graph.gexf --format json --output graph.json

# For Gephi / graph tools
grph export graph.gexf --format graphml --output graph.graphml
```

## Available Formats

| Format | Best For | Command |
|--------|----------|---------|
| **JSON** | D3.js, web apps, JavaScript | `--format json` |
| **GraphML** | Gephi, yEd, graph tools | `--format graphml` |
| **Adjacency List** | Simple tools, scripts | `--format adjlist` |
| **Edge List** | CSV import, spreadsheets | `--format edgelist` |

## Examples

### Export for D3.js

```bash
grph export social-network.gexf --format json --output network.json
```

The JSON output uses the node-link format that D3.js expects:

```json
{
  "nodes": [{"id": "user1", "label": "@user1", ...}],
  "links": [{"source": "user1", "target": "user2", ...}]
}
```

### Export Subgraph for Focused Visualization

First extract a subgraph, then export:

```bash
# Extract ego network
grph ego large-graph.gexf central-node --radius 2 --output subset.gexf

# Export for visualization
grph export subset.gexf --format json --output subset.json
```

### Export to Standard Output

Omit `--output` to print to stdout:

```bash
grph export graph.gexf --format edgelist
```

## Using with Gephi

1. Export to GraphML:
   ```bash
   grph export graph.gexf --format graphml --output graph.graphml
   ```

2. Open Gephi and use File → Open → Select the .graphml file

3. Apply layouts and styling in Gephi

## Using with D3.js

```javascript
// Load the exported JSON
d3.json("network.json").then(data => {
  // data.nodes and data.links are ready for force simulation
  const simulation = d3.forceSimulation(data.nodes)
    .force("link", d3.forceLink(data.links).id(d => d.id))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));
});
```

## Related

- [Extract Subgraphs](./extract-subgraphs) - Create focused views first
- `grph export --help` - Full command documentation
