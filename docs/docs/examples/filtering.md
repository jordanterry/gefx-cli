---
sidebar_position: 1
title: Filtering Examples
---

# Filtering Examples

This page shows practical examples of using grph CLI's filtering capabilities to find specific nodes and edges in your graphs.

## Node Filtering

### By Single Attribute

Find all nodes of a specific type:

```bash
grph nodes network.gexf --attr type=server
```

### By Multiple Attributes (AND)

Find servers with a specific weight:

```bash
grph nodes network.gexf --attr type=server --attr weight=2.0
```

Both conditions must be true for a node to match.

### By Label Pattern

Find nodes with labels starting with "Web":

```bash
grph nodes network.gexf --label "Web*"
```

Find nodes with labels containing "Server":

```bash
grph nodes network.gexf --label "*Server*"
```

Find nodes with labels matching a pattern:

```bash
grph nodes network.gexf --label "Server[12]"  # Matches Server1 or Server2
```

### Combine Attribute and Label Filters

Find servers with labels starting with "Production":

```bash
grph nodes network.gexf --attr type=server --label "Production*"
```

## Edge Filtering

### By Source Node

Find all edges originating from a specific node:

```bash
grph edges network.gexf --source loadbalancer1
```

### By Target Node

Find all edges pointing to a specific node:

```bash
grph edges network.gexf --target database1
```

### By Both Source and Target

Check if there's a direct connection between two nodes:

```bash
grph edges network.gexf --source server1 --target database1
```

### By Attribute

Find edges with a specific relationship:

```bash
grph edges network.gexf --attr relationship=queries
```

### Complex Edge Queries

Find all query edges from server1:

```bash
grph edges network.gexf --source server1 --attr relationship=queries
```

Find heavy-weight edges to the database:

```bash
grph edges network.gexf --target database1 --attr weight=2.0
```

## Real-World Scenarios

### Infrastructure Analysis

**Find all database connections:**

```bash
grph edges infra.gexf --attr relationship=queries
```

**Find all nodes in a specific tier:**

```bash
grph nodes infra.gexf --attr tier=frontend
```

**Find all connections to a specific service:**

```bash
grph edges infra.gexf --target api-gateway
```

### Social Network Analysis

**Find all users in a community:**

```bash
grph nodes social.gexf --attr community=tech
```

**Find all connections of a specific type:**

```bash
grph edges social.gexf --attr type=follows
```

**Find connections from a specific user:**

```bash
grph edges social.gexf --source user123
```

### Dependency Analysis

**Find all direct dependencies of a package:**

```bash
grph edges deps.gexf --source my-package
```

**Find all packages that depend on a library:**

```bash
grph edges deps.gexf --target lodash
```

**Find dev dependencies:**

```bash
grph edges deps.gexf --attr scope=dev
```

## Tips

### No Results?

If your filter returns no results:

1. Check available attributes with `grph info`:
   ```bash
   grph info graph.gexf
   ```

2. List all nodes/edges first to see what values exist:
   ```bash
   grph nodes graph.gexf
   grph edges graph.gexf
   ```

3. Attribute matching is **case-sensitive** and **exact**:
   - `--attr type=Server` won't match `type=server`
   - `--attr weight=1` won't match `weight=1.0`

### Checking Specific Values

Use JSON output with `jq` to explore unique values:

```bash
# Find all unique node types
grph nodes graph.gexf --json | jq '[.[].attributes.type] | unique'

# Find all unique edge relationships
grph edges graph.gexf --json | jq '[.[].attributes.relationship] | unique'
```

### Complex Filtering with jq

For queries that grph CLI doesn't support directly (like numeric comparisons or OR logic), use JSON output with `jq`:

```bash
# Nodes with weight > 1.0
grph nodes graph.gexf --json | jq '[.[] | select(.attributes.weight > 1.0)]'

# Edges with weight between 1.0 and 2.0
grph edges graph.gexf --json | jq '[.[] | select(.weight >= 1.0 and .weight <= 2.0)]'

# Nodes of type "server" OR "database"
grph nodes graph.gexf --json | jq '[.[] | select(.attributes.type == "server" or .attributes.type == "database")]'
```
