---
sidebar_position: 4
title: Analyzing npm Dependencies
---

# Analyzing npm Dependencies

In this tutorial, you'll explore a React application's dependency graph. You'll learn to trace dependency chains, find what depends on a package, detect deprecated packages, and understand the hidden complexity in your node_modules.

**Level:** Intermediate
**Time:** 20 minutes
**Prerequisites:** Familiarity with npm/JavaScript ecosystem helpful

## What You'll Learn

- Tracing dependency chains from app to leaf packages
- Finding reverse dependencies (what depends on X?)
- Detecting deprecated or problematic packages
- Understanding transitive dependencies
- Analyzing package importance in your dependency tree

## The Dataset

The `npm-dependencies.gexf` file represents a typical React application:

- **38 packages** including React, Redux, testing libraries, and build tools
- **51 dependency relationships** (both direct and transitive)
- **Node attributes**: version, type (library/dev), weekly downloads, deprecated status
- **Edge attributes**: dependency type (dependency/devDependency/peerDependency), version constraint

## Step 1: Understand Your Dependencies

Let's see what we're working with:

```bash
grph info examples/npm-dependencies.gexf
```

```
                    Graph Summary
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Property          ┃ Value                          ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ File              │ examples/npm-dependencies.gexf │
│ Version           │ 1.3                            │
│ Mode              │ static                         │
│ Default Edge Type │ directed                       │
│ Node Count        │ 38                             │
│ Edge Count        │ 51                             │
└───────────────────┴────────────────────────────────┘

Node Attributes: deprecated, downloads_weekly, type, version
```

This is a **directed graph** where edges point from a package to its dependencies. If A → B, then A depends on B.

## Step 2: See Your Direct Dependencies

What does your application directly depend on?

```bash
grph neighbors examples/npm-dependencies.gexf my-app --direction out
```

You'll see a list of direct dependencies including:
- React and React DOM
- Redux Toolkit and React Redux
- React Router DOM
- Axios, Lodash, Formik, and more
- Dev dependencies like TypeScript, Vite, Jest, and ESLint

### Count Your Dependencies

How many direct dependencies does the app have?

```bash
grph neighbors examples/npm-dependencies.gexf my-app --direction out --json | grep '"id"' | wc -l
```

This counts the packages. You might be surprised how many there are!

## Step 3: Find Deprecated Packages

This is critical for maintenance. Let's find any deprecated packages:

```bash
grph nodes examples/npm-dependencies.gexf --attr deprecated=True
```

```
                                   Nodes (1)
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID      ┃ Label   ┃ Attributes                                               ┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ request │ request │ version=2.88.2, type=library, downloads_weekly=20000000, │
│         │         │ deprecated=True                                          │
└─────────┴─────────┴──────────────────────────────────────────────────────────┘
```

The `request` package is deprecated. This is a real issue - `request` was one of npm's most popular packages but was deprecated in 2020.

### Is Your App Affected?

Check if your app depends on this deprecated package:

```bash
grph has-path examples/npm-dependencies.gexf my-app request
```

```
Path exists: Yes
```

You're using a deprecated package. Let's see how:

```bash
grph path examples/npm-dependencies.gexf my-app request
```

```
Path from my-app to request
Length: 1 edge

Path: my-app → request
```

It's a direct dependency! This needs to be replaced.

## Step 4: Trace Dependency Chains

Let's understand the full dependency chain for a package. What does React actually pull in?

```bash
grph reachable examples/npm-dependencies.gexf react --max-depth 3
```

This shows all packages that React depends on (directly or transitively).

### Follow the Chain

Let's trace from your app down to a leaf package like `js-tokens`:

```bash
grph path examples/npm-dependencies.gexf my-app js-tokens
```

```
Path from my-app to js-tokens
Length: 3 edges

Path: my-app → react → loose-envify → js-tokens
```

You can see how your app → react → loose-envify → js-tokens. Three levels deep!

## Step 5: Find What Depends on a Package

Reverse dependency analysis: what breaks if we change a package?

### What Uses React?

```bash
grph neighbors examples/npm-dependencies.gexf react --direction in
```

This shows all packages that depend on React:
- Your app (my-app)
- react-dom (peer dependency)
- react-redux (peer dependency)
- And more...

### Impact Analysis

If we needed to upgrade React, how many packages would be affected?

```bash
grph neighbors examples/npm-dependencies.gexf react --direction in --json | grep '"id"' | wc -l
```

This is crucial for planning major version upgrades.

## Step 6: Identify Core Packages

Which packages are most important in your dependency tree? Use centrality:

```bash
grph centrality examples/npm-dependencies.gexf --type pagerank --top 10
```

This uses PageRank to find packages that many other packages depend on. These are your "core" dependencies.

### Find Bridge Packages

Betweenness centrality finds packages that connect different parts of your dependency tree:

```bash
grph centrality examples/npm-dependencies.gexf --type betweenness --top 5
```

High betweenness packages are often adapters or utilities that many different packages use.

## Step 7: Analyze Dependency Types

Let's look at the edges to understand dependency types:

```bash
grph edges examples/npm-dependencies.gexf --source my-app
```

You'll see dependencies marked as `dependency`, `devDependency`, or `peerDependency`.

### Find All Peer Dependencies

Peer dependencies are special - they expect the parent project to provide them:

```bash
grph edges examples/npm-dependencies.gexf --json | grep -A2 '"peerDependency"'
```

Understanding peer dependencies helps avoid version conflicts.

## Step 8: Separate Dev Dependencies

Which packages are only needed for development?

```bash
grph nodes examples/npm-dependencies.gexf --attr type=dev
```

This shows packages like Jest, TypeScript, Vite, ESLint, and Prettier. These don't ship with your production bundle.

### Production Dependencies Only

```bash
grph nodes examples/npm-dependencies.gexf --attr type=library
```

These are the packages that actually end up in your production build.

## Step 9: Analyze Build Tool Dependencies

Let's trace what Vite pulls in:

```bash
grph neighbors examples/npm-dependencies.gexf vite --direction out
```

```
Neighbors of vite (depth=1, direction=out)

┃ ID      ┃ Label   ┃
├─────────┼─────────┤
│ esbuild │ esbuild │
│ rollup  │ rollup  │
```

Vite depends on both esbuild (for dev) and rollup (for production builds).

## Step 10: Get Statistics

Finally, let's understand the overall structure:

```bash
grph stats examples/npm-dependencies.gexf
```

This shows:
- Network density (how interconnected packages are)
- Whether the dependency graph is a DAG (directed acyclic graph) - it should be!
- Average number of dependencies per package

## What You've Learned

You've mastered dependency analysis:

- **Direct vs transitive dependencies**: Understanding the full chain
- **Reverse dependencies**: Finding what depends on a package
- **Deprecated package detection**: Finding maintenance issues
- **Centrality for importance**: Identifying core packages
- **Dependency types**: Understanding peer, dev, and regular dependencies

## Real-World Applications

This approach works for any dependency system:

- **Python (pip)**: Analyze requirements.txt as a graph
- **Java (Maven/Gradle)**: Trace dependency trees
- **Go modules**: Understand go.mod relationships
- **Dagger/DI frameworks**: Analyze injection graphs

## Next Steps

- Try the [Social Network tutorial](./social-network) for social graph analysis
- See how to [detect circular dependencies](../how-to/detect-circular-dependencies)
- Learn about [exporting for visualization](../how-to/export-for-visualization)

## Exercises

1. **Find the package with the most weekly downloads**:
   Look at the `downloads_weekly` attribute and use `grph nodes --json` with `jq` to sort.

2. **How many packages does React Redux ultimately depend on?**
   ```bash
   grph reachable examples/npm-dependencies.gexf react-redux --max-depth 5
   ```

3. **Find all testing-related packages**:
   ```bash
   grph nodes examples/npm-dependencies.gexf --label "@testing-library"
   ```

4. **What's the longest dependency chain in this project?**
   Try `grph all-paths` between `my-app` and various leaf packages like `js-tokens` or `@emotion/memoize`.
