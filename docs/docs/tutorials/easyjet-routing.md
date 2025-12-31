---
sidebar_position: 3
title: Routing EasyJet Crew Across Europe
---

# Routing EasyJet Crew Across Europe

In this tutorial, you'll help plan crew routes across EasyJet's European network. You'll work with a directed, weighted graph representing flight routes, learning how direction and weights affect path finding.

**Level:** Intermediate
**Time:** 20 minutes
**Prerequisites:** Completed the [London Underground tutorial](./london-underground)

## What You'll Learn

- Working with **directed graphs** (flights go one way)
- Using **weighted edges** for optimization
- Finding routes with multiple connections
- Analyzing hub airport connectivity
- Finding all reachable destinations

## The Scenario

You're helping EasyJet's crew scheduling team. A crew member based in London Luton needs to get to Dubrovnik for an assignment. The challenge: there's no direct flight. You need to find a route using EasyJet's network.

## The Dataset

The `easyjet-routes.gexf` file contains:

- **30 airports** across the UK and Europe
- **86 flight routes** with direction (origin → destination)
- **Node attributes**: city, country, hub status, IATA code
- **Edge attributes**: flight time (hours), distance (km), weekly frequency

## Step 1: Understand the Network

Let's start by examining the network:

```bash
grph info examples/easyjet-routes.gexf
```

```
                   Graph Summary
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Property          ┃ Value                        ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ File              │ examples/easyjet-routes.gexf │
│ Version           │ 1.3                          │
│ Mode              │ static                       │
│ Default Edge Type │ directed                     │
│ Node Count        │ 30                           │
│ Edge Count        │ 86                           │
└───────────────────┴──────────────────────────────┘
```

**Key difference from the Underground**: This graph is **directed**. A flight from London to Barcelona doesn't automatically mean there's a flight back. This is realistic - some routes are seasonal or one-way only.

## Step 2: Find Hub Airports

Hub airports have the most connections. Let's identify EasyJet's hubs:

```bash
grph nodes examples/easyjet-routes.gexf --attr hub=True
```

You'll see 16 hub airports including London Luton (LTN), London Gatwick (LGW), Amsterdam (AMS), Barcelona (BCN), and others.

### Analyze Hub Connectivity

Which hubs have the most outgoing flights? Use degree centrality with the `out` direction:

```bash
grph degree examples/easyjet-routes.gexf --direction out --top 5
```

This shows which airports you can fly TO the most destinations from.

Now check incoming flights:

```bash
grph degree examples/easyjet-routes.gexf --direction in --top 5
```

This shows which airports receive the most flights - useful for crew positioning.

## Step 3: Route Crew to Dubrovnik

Now for our main task: get a crew member from London Luton (LTN) to Dubrovnik (DBV).

First, check if there's a direct flight:

```bash
grph has-path examples/easyjet-routes.gexf LTN DBV
```

```
Path exists: Yes
```

There's a path. Let's find it:

```bash
grph path examples/easyjet-routes.gexf LTN DBV
```

```
Path from LTN to DBV
Length: 3 edges

Path: LTN → EDI → LGW → DBV
```

Interesting! The route goes via Edinburgh and Gatwick. Let's find alternative routes.

## Step 4: Find Alternative Routes

Maybe there's a shorter route. Use `all-paths` to find alternatives:

```bash
grph all-paths examples/easyjet-routes.gexf LTN DBV --max-depth 4
```

This finds all simple paths with up to 4 connections. You might see routes via different hubs like Amsterdam or Barcelona.

### Understanding Direction

Let's check what destinations are directly reachable from Luton:

```bash
grph neighbors examples/easyjet-routes.gexf LTN --direction out
```

The `--direction out` flag is crucial for directed graphs. It shows where you can fly TO from Luton. Compare with:

```bash
grph neighbors examples/easyjet-routes.gexf LTN --direction in
```

This shows where you can fly FROM to reach Luton - useful for return journeys.

## Step 5: Analyze Reachability

Where can crew get to from Luton with one connection? Use `reachable`:

```bash
grph reachable examples/easyjet-routes.gexf LTN --max-depth 2
```

This shows all airports reachable with up to 2 flights (direct + one connection).

### Check Specific Destinations

Can we reach Athens (ATH) from Luton?

```bash
grph has-path examples/easyjet-routes.gexf LTN ATH && grph path examples/easyjet-routes.gexf LTN ATH
```

What about Corfu (CFU)?

```bash
grph path examples/easyjet-routes.gexf LTN CFU
```

## Step 6: Find Strategic Connections

Which airports are most important for connecting the network? Use betweenness centrality:

```bash
grph centrality examples/easyjet-routes.gexf --type betweenness --top 5
```

Airports with high betweenness are critical connection points. If one of these airports had problems, many routes would be disrupted.

### PageRank for Importance

PageRank considers both the number and quality of connections:

```bash
grph centrality examples/easyjet-routes.gexf --type pagerank --top 5
```

This often surfaces airports that are well-connected to OTHER well-connected airports.

## Step 7: Filter by Country

Let's see all Spanish airports in the network:

```bash
grph nodes examples/easyjet-routes.gexf --attr country=Spain
```

What about UK airports?

```bash
grph nodes examples/easyjet-routes.gexf --attr country=UK
```

## Step 8: Analyze Route Details

Let's look at the actual flight connections using edges:

```bash
grph edges examples/easyjet-routes.gexf --source LTN
```

This shows all flights departing from Luton, including their attributes like flight time and frequency.

Filter for longer flights:

```bash
grph edges examples/easyjet-routes.gexf --source LTN --json | head -30
```

The JSON output lets you pipe to tools like `jq` for advanced filtering.

## Step 9: Network Statistics

Get an overview of network characteristics:

```bash
grph stats examples/easyjet-routes.gexf
```

This shows:
- How connected the network is
- Whether it's strongly connected (can get anywhere from anywhere)
- Network density and structure

## What You've Learned

You've mastered working with directed, weighted graphs:

- **Direction matters**: `--direction in` vs `--direction out` for analyzing flows
- **Path finding**: Finding routes when direct connections don't exist
- **Reachability**: Understanding what's accessible within N steps
- **Hub analysis**: Identifying critical connection points
- **Filtering**: Finding nodes by country, hub status, and other attributes

## Real-World Applications

This same approach works for:

- **Logistics networks**: Shipping routes, delivery networks
- **Communication networks**: Data routing, network topology
- **Supply chains**: Supplier → manufacturer → distributor flows
- **Any directed flow system**: Water, electricity, information

## Next Steps

- Try the [npm Dependencies tutorial](./npm-dependencies) for software dependency analysis
- Learn about [centrality metrics](../explanation/centrality-metrics) in depth
- See how to [export graphs for visualization](../how-to/export-for-visualization)

## Exercises

1. **Find all routes from Bristol (BRS) to Athens (ATH)**:
   ```bash
   grph all-paths examples/easyjet-routes.gexf BRS ATH --max-depth 4
   ```

2. **Which airport can reach the most destinations directly?**
   Use degree centrality with `--direction out`.

3. **Find airports that are reachable from Luton but can't fly back directly to Luton**:
   Compare `grph reachable LTN --max-depth 1` with `grph neighbors LTN --direction in`.

4. **Create a subgraph of just UK airports**:
   ```bash
   grph subgraph examples/easyjet-routes.gexf LTN LGW STN BRS EDI MAN BFS
   ```
