---
sidebar_position: 4
title: When to Use grph
---

# When to Use grph

grph is a command-line tool for exploring and analyzing graph data. This article helps you understand when graph analysis is the right approach and when grph is the right tool.

## What Problems Suit Graph Analysis?

Graph analysis shines when your data involves **relationships** between entities. If you can phrase your question as "how does X relate to Y?", graphs might help.

### Good Fit: Relationship Questions

- "What depends on this package?"
- "How can I get from A to B?"
- "Who is most influential?"
- "What connects these two things?"
- "What's the impact if this node fails?"

### Less Good Fit: Aggregate Questions

- "What's the total sales this quarter?" (use SQL/analytics)
- "What's the average response time?" (use monitoring tools)
- "How many users signed up?" (use databases)

## Real-World Use Cases

### Software Development

**Dependency Analysis**
- "What breaks if I upgrade lodash?"
- "Are there circular dependencies?"
- "What's the dependency chain to this package?"

**Architecture Understanding**
- "Which services call which?"
- "What's the blast radius of this API change?"
- "Which modules are most coupled?"

```bash
# Find what depends on a critical package
grph neighbors dependencies.gexf lodash --direction in --depth 2

# Check for cycles
grph components dependencies.gexf --type strongly --list
```

### DevOps & Infrastructure

**Network Topology**
- "What's the path from client to database?"
- "Which routers are single points of failure?"
- "What's affected if this node goes down?"

**Service Mesh Analysis**
- "How do requests flow through the system?"
- "Which services are most critical?"

```bash
# Find critical network nodes
grph centrality network.gexf --type betweenness --top 10

# Trace request path
grph path services.gexf api-gateway database
```

### Data Engineering

**Lineage Tracking**
- "Where does this data come from?"
- "What downstream systems use this table?"
- "What's the transformation path?"

```bash
# Find data sources
grph neighbors lineage.gexf final-report --direction in --depth 5

# Find downstream impact
grph neighbors lineage.gexf raw-data --direction out --depth 5
```

### Research & Analysis

**Citation Networks**
- "What are the foundational papers in this field?"
- "How are these research areas connected?"

**Collaboration Networks**
- "Who are the key collaborators?"
- "Which groups work together?"

```bash
# Find influential papers
grph centrality citations.gexf --type pagerank --top 20
```

### Social & Organizational

**Influence Analysis**
- "Who are the key influencers?"
- "How connected are two people?"

**Organizational Analysis**
- "Who are the bridges between teams?"
- "What's the communication structure?"

```bash
# Find organizational connectors
grph centrality org-network.gexf --type betweenness --top 10

# Find common connections
grph common-neighbors org.gexf person-a person-b
```

## Why Command Line?

grph is a CLI tool. This is intentional:

### Strengths of CLI

1. **Scriptable**: Chain with other tools, automate analysis
2. **Fast**: No GUI overhead, quick answers
3. **Reproducible**: Commands can be documented and rerun
4. **Piping**: Use with `jq`, `grep`, shell scripts
5. **CI/CD Integration**: Add graph checks to pipelines

```bash
# Script example: Check for deprecated dependencies
grph nodes deps.gexf --attr deprecated=True --json | jq '.[].id' > deprecated.txt
if [ -s deprecated.txt ]; then
  echo "Warning: Deprecated packages found"
  cat deprecated.txt
fi
```

### When You Might Want Something Else

- **Visualization**: Export to Gephi, D3.js, or other tools
- **Complex queries**: Graph databases like Neo4j offer query languages
- **Real-time analysis**: Streaming graph tools for live data
- **Very large graphs**: Distributed systems like Apache Spark GraphX

## The grph Philosophy

**Like grep, but for graphs.**

Just as `grep` lets you quickly search text files, grph lets you quickly explore graph files. It's designed for:

- Quick answers to graph questions
- Exploration of unknown graph data
- Integration with other command-line tools
- Simple, focused functionality

## Getting Started

If you have graph data and relationship questions, give grph a try:

```bash
# Install
pip install grph-cli

# Explore your data
grph info your-graph.gexf
grph nodes your-graph.gexf
grph stats your-graph.gexf

# Start asking questions
grph neighbors your-graph.gexf interesting-node
grph centrality your-graph.gexf --type pagerank --top 10
```

The tutorials in this documentation use realistic examples that demonstrate grph's capabilities.
