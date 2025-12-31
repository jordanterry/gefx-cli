---
sidebar_position: 2
title: Exploring the London Underground
---

# Exploring the London Underground

In this tutorial, you'll learn the basics of grph by exploring a graph of the London Underground network. By the end, you'll be able to load graphs, explore their structure, find paths between stations, and identify the busiest interchanges.

**Level:** Beginner
**Time:** 15 minutes
**Prerequisites:** grph installed, example files available

## What You'll Learn

- Loading and inspecting a GEXF graph file
- Listing nodes (stations) and their attributes
- Filtering nodes by attributes
- Finding the shortest path between stations
- Identifying important nodes using centrality

## The Dataset

The `london-underground.gexf` file contains a subset of Central London's Tube network:

- **22 stations** including major interchanges like Oxford Circus, King's Cross, and Bank
- **36 connections** between stations
- **Attributes** include zone, lines served, and whether a station is an interchange
- **Edge weights** represent travel time in minutes

## Step 1: Get an Overview

First, let's see what we're working with. The `info` command gives you a quick summary:

```bash
grph info examples/london-underground.gexf
```

You should see output like:

```
                     Graph Summary
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Property          ┃ Value                            ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ File              │ examples/london-underground.gexf │
│ Version           │ 1.3                              │
│ Mode              │ static                           │
│ Default Edge Type │ undirected                       │
│ Node Count        │ 22                               │
│ Edge Count        │ 36                               │
└───────────────────┴──────────────────────────────────┘

Node Attributes: interchange, lines, zone
Edge Attributes: id, line, time_minutes
```

**Key observations:**
- The graph is **undirected** - you can travel in both directions on the Tube
- There are **22 stations** connected by **36 track sections**
- Nodes have attributes like `zone`, `lines`, and `interchange`
- Edges have `time_minutes` - the travel time between stations

## Step 2: List All Stations

Let's see all the stations in our network:

```bash
grph nodes examples/london-underground.gexf
```

This displays a table of all nodes with their IDs, labels, and attributes:

```
                                   Nodes (22)
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID                    ┃ Label                     ┃ Attributes                ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ oxford-circus         │ Oxford Circus             │ zone=1,                   │
│                       │                           │ lines=Central,Victoria,B… │
│                       │                           │ interchange=True          │
│ tottenham-court-road  │ Tottenham Court Road      │ zone=1,                   │
│                       │                           │ lines=Central,Northern,E… │
│                       │                           │ interchange=True          │
...
```

Notice each station has:
- **zone**: Which fare zone it's in (all Zone 1 in this dataset)
- **lines**: Which Tube lines serve this station
- **interchange**: Whether you can change lines here

## Step 3: Find Interchange Stations

Let's filter to show only interchange stations - places where you can change lines:

```bash
grph nodes examples/london-underground.gexf --attr interchange=True
```

This filters the list to show only stations where `interchange` is `True`. You'll see major stations like Oxford Circus, King's Cross, and Bank.

Try finding stations that are NOT interchanges:

```bash
grph nodes examples/london-underground.gexf --attr interchange=False
```

You should see stations like Chancery Lane, Covent Garden, and Russell Square - single-line stations.

## Step 4: Find a Route

Now for the fun part - finding routes between stations! Let's plan a journey from King's Cross to Bank:

```bash
grph path examples/london-underground.gexf kings-cross bank
```

Output:
```
Path from kings-cross to bank
Length: 4 edges

Path: kings-cross → russell-square → holborn → chancery-lane → bank
```

grph found the shortest path: 4 stops via the Piccadilly and Central lines.

### Try Different Routes

Find a path from Oxford Circus to Waterloo:

```bash
grph path examples/london-underground.gexf oxford-circus waterloo
```

What about from Baker Street to London Bridge?

```bash
grph path examples/london-underground.gexf baker-street london-bridge
```

## Step 5: Explore Connections

What stations are directly connected to Oxford Circus? Use the `neighbors` command:

```bash
grph neighbors examples/london-underground.gexf oxford-circus
```

This shows all stations one stop away from Oxford Circus. You should see stations like Tottenham Court Road, Bond Street, Warren Street, Green Park, and Piccadilly Circus.

### Go Deeper

To see stations within 2 stops, use the `--depth` option:

```bash
grph neighbors examples/london-underground.gexf oxford-circus --depth 2
```

This expands the search to include stations two stops away.

## Step 6: Find the Busiest Interchanges

Which stations have the most connections? We can use centrality analysis to find out:

```bash
grph centrality examples/london-underground.gexf --type degree --top 5
```

Output:
```
     Degree Centrality (Top 5)
┏━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Rank ┃ Node          ┃ Score    ┃
┡━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ 1    │ oxford-circus │ 0.285714 │
│ 2    │ green-park    │ 0.238095 │
│ 3    │ embankment    │ 0.238095 │
│ 4    │ holborn       │ 0.190476 │
│ 5    │ euston        │ 0.190476 │
└──────┴───────────────┴──────────┘
```

Oxford Circus is the most connected station - no surprise to anyone who's been crushed in the crowds there!

### Understanding Centrality

**Degree centrality** measures how many direct connections a node has. Higher scores mean more connections. In a transport network, high-degree stations are natural interchange points.

Try **betweenness centrality** to find stations that are critical for routing:

```bash
grph centrality examples/london-underground.gexf --type betweenness --top 5
```

Betweenness measures how often a station appears on the shortest path between other stations. High betweenness stations are critical - if they closed, many journeys would be disrupted.

## Step 7: Get Network Statistics

Finally, let's get an overall view of the network structure:

```bash
grph stats examples/london-underground.gexf
```

This shows statistics like:
- **Density**: How interconnected the network is (1.0 = every station connected to every other)
- **Average degree**: Average number of connections per station
- **Connected**: Whether you can get from any station to any other

## What You've Learned

Congratulations! You've learned how to:

- **Load a graph** with `grph info` to see its structure
- **List nodes** with `grph nodes` and filter by attributes
- **Find paths** with `grph path` for journey planning
- **Explore neighborhoods** with `grph neighbors`
- **Analyze importance** with `grph centrality`
- **Get statistics** with `grph stats`

## Next Steps

- Try the [EasyJet Routing tutorial](./easyjet-routing) to work with directed, weighted graphs
- Learn about [centrality metrics](../explanation/centrality-metrics) in depth
- See the [CLI Reference](../cli-reference/) for all available commands

## Exercises

1. **Find the path from Westminster to Liverpool Street.** How many stops is it?

2. **Which stations are reachable from Piccadilly Circus within 3 stops?**
   ```bash
   grph neighbors examples/london-underground.gexf piccadilly-circus --depth 3
   ```

3. **Export the network to JSON** for visualization in a tool like D3.js:
   ```bash
   grph export examples/london-underground.gexf --format json
   ```

4. **Find all simple paths between Oxford Circus and Bank** (there might be more than one!):
   ```bash
   grph all-paths examples/london-underground.gexf oxford-circus bank --max-depth 6
   ```
