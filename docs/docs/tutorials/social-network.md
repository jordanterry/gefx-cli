---
sidebar_position: 5
title: Finding Influencers in a Social Network
---

# Finding Influencers in a Social Network

In this advanced tutorial, you'll analyze a social network to find influential users, discover communities, and understand network dynamics. You'll apply multiple centrality metrics and learn when to use each one.

**Level:** Advanced
**Time:** 25 minutes
**Prerequisites:** Completed previous tutorials, understanding of graph concepts

## What You'll Learn

- Applying multiple centrality metrics (degree, betweenness, PageRank, eigenvector)
- Finding mutual connections between users
- Analyzing verified vs non-verified users
- Understanding follow patterns and influence
- Extracting ego networks around key users

## The Dataset

The `social-network.gexf` file represents a tech-focused social network:

- **23 users** ranging from major influencers to new accounts
- **88 follow relationships** (directed: follower → followed)
- **Node attributes**: display name, follower count, following count, verified status, category, join year
- **Edge attributes**: year the follow happened, interaction score

## Step 1: Explore the Network

Let's understand what we're working with:

```bash
grph info examples/social-network.gexf
```

```
                   Graph Summary
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Property          ┃ Value                        ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ File              │ examples/social-network.gexf │
│ Version           │ 1.3                          │
│ Mode              │ static                       │
│ Default Edge Type │ directed                     │
│ Node Count        │ 23                           │
│ Edge Count        │ 88                           │
└───────────────────┴──────────────────────────────┘

Node Attributes: category, display_name, followers, following, joined_year, verified
```

Key observation: this is a **directed** graph. A follow from A → B means A follows B (A sees B's content). The direction matters!

## Step 2: Find Verified Accounts

Let's start by finding verified users - these are typically established influencers:

```bash
grph nodes examples/social-network.gexf --attr verified=True
```

You'll see accounts like @techguru, @codequeen, @airesearcher, and companies like @techcompany.

### Compare with Non-Verified

```bash
grph nodes examples/social-network.gexf --attr verified=False
```

These include newer accounts like @juniordev, @bootcamper, @student, and @hobbyist.

## Step 3: Find Top Influencers

Now the core question: who are the most influential users? Let's use multiple centrality metrics and compare.

### Method 1: PageRank (Network Influence)

PageRank measures influence based on who follows you AND how influential those followers are:

```bash
grph centrality examples/social-network.gexf --type pagerank --top 5
```

```
   Pagerank Centrality (Top 5)
┏━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Rank ┃ Node        ┃ Score    ┃
┡━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ 1    │ codequeen   │ 0.125834 │
│ 2    │ techguru    │ 0.085864 │
│ 3    │ pythonista  │ 0.069127 │
│ 4    │ frontenddev │ 0.066747 │
│ 5    │ devtools    │ 0.064617 │
└──────┴─────────────┴──────────┘
```

Interesting! @codequeen ranks higher than @techguru despite having fewer raw followers. Why? Because she's followed by other influential accounts.

### Method 2: In-Degree (Raw Follower Count in Network)

How many accounts in our network follow each user?

```bash
grph degree examples/social-network.gexf --direction in --top 5
```

This measures direct "popularity" within our network sample.

### Method 3: Betweenness (Bridge Position)

Who connects different parts of the network?

```bash
grph centrality examples/social-network.gexf --type betweenness --top 5
```

Users with high betweenness bridge different communities. They might connect tech influencers with business accounts, or established users with newcomers.

### Method 4: Eigenvector (Well-Connected to Well-Connected)

Similar to PageRank but considers the full network more equally:

```bash
grph centrality examples/social-network.gexf --type eigenvector --top 5
```

Compare all four methods - do the same accounts appear across metrics, or are there differences?

## Step 4: Analyze User Categories

Let's see the different types of users:

### Tech Accounts
```bash
grph nodes examples/social-network.gexf --attr category=tech
```

### Business/Startup Accounts
```bash
grph nodes examples/social-network.gexf --attr category=business
```

### Media Accounts
```bash
grph nodes examples/social-network.gexf --attr category=media
```

### Company Accounts
```bash
grph nodes examples/social-network.gexf --attr category=company
```

## Step 5: Find Mutual Connections

A key social network feature: finding users that both follow and are followed by someone (mutual follows), or finding common connections between two users.

### Common Followers

Who do both @techguru and @codequeen follow? These are their common connections:

```bash
grph common-neighbors examples/social-network.gexf techguru codequeen
```

```
Common neighbors of techguru and codequeen

┃ ID             ┃ Label           ┃
├────────────────┼─────────────────┤
│ careerswitcher │ @careerswitcher │
│ podcasthost    │ @podcasthost    │
```

Both major influencers follow @podcasthost - probably a popular tech podcast!

### Find More Common Connections

Try different pairs:

```bash
grph common-neighbors examples/social-network.gexf startupfounder vcpartner
```

What connections do the startup ecosystem accounts share?

## Step 6: Analyze Follow Patterns

Let's look at who key accounts follow:

### Who Does @techguru Follow?

```bash
grph neighbors examples/social-network.gexf techguru --direction out
```

This shows the accounts that @techguru follows (their outgoing edges).

### Who Follows @codequeen?

```bash
grph neighbors examples/social-network.gexf codequeen --direction in
```

This shows accounts that follow @codequeen (incoming edges = followers).

### Compare Follower Counts

Some accounts follow few but are followed by many (influencers), while others follow many but have few followers (consumers):

```bash
grph nodes examples/social-network.gexf --json | head -50
```

Look at the `followers` and `following` attributes - the ratio tells you a lot about an account.

## Step 7: Trace Connection Paths

How are two users connected? Let's trace paths:

### New User to Influencer

How is @student connected to @techguru?

```bash
grph path examples/social-network.gexf student techguru
```

This shows the follow chain from @student to @techguru.

### Can Newcomers Reach Everyone?

```bash
grph has-path examples/social-network.gexf student techcompany
```

Check if there's any path from a new account to a major company account.

## Step 8: Extract Ego Networks

An "ego network" is the network around a specific user. Let's extract @codequeen's network:

```bash
grph ego examples/social-network.gexf codequeen --radius 1
```

This shows @codequeen and everyone directly connected (followers and following).

### Expand the Network

Include connections of connections:

```bash
grph ego examples/social-network.gexf codequeen --radius 2
```

This reveals the extended network - often called "friends of friends."

## Step 9: Find Newcomer Growth Paths

Let's help new accounts understand who to follow for growth.

### Who Should @bootcamper Follow?

Find influential accounts that might follow back (those who follow newcomers):

```bash
# Who does @codequeen follow? (She follows some newcomers)
grph neighbors examples/social-network.gexf codequeen --direction out
```

Notice that @codequeen follows @juniordev and @careerswitcher - she engages with newcomers!

### Trace Successful Newcomers

Who does @careerswitcher follow? They grew from 0 to 8500 followers:

```bash
grph neighbors examples/social-network.gexf careerswitcher --direction out
```

## Step 10: Network Statistics

Finally, let's understand the overall network structure:

```bash
grph stats examples/social-network.gexf
```

Key metrics to look for:
- **Density**: How interconnected is the network?
- **Average path length**: How many "degrees of separation" on average?
- **Clustering**: Do friends tend to be friends with each other?

## Comparing Centrality Metrics

Here's a summary of when to use each metric:

| Metric | Measures | Best For |
|--------|----------|----------|
| **PageRank** | Influence from quality followers | Finding true influencers |
| **In-Degree** | Raw follower count | Simple popularity |
| **Out-Degree** | How many they follow | Finding active engagers |
| **Betweenness** | Bridge position | Finding connectors |
| **Eigenvector** | Connected to connected | Finding inner circle |

## What You've Learned

You've mastered social network analysis:

- **Multiple centrality metrics**: Understanding different types of influence
- **Mutual connections**: Finding shared relationships
- **Follow pattern analysis**: Understanding account behavior
- **Ego networks**: Extracting networks around key users
- **Path tracing**: Understanding connection chains

## Real-World Applications

These techniques apply to:

- **Marketing**: Finding influencers for campaigns
- **Community building**: Understanding network structure
- **HR/Recruiting**: Mapping professional networks
- **Research**: Academic citation and collaboration networks
- **Security**: Detecting bot networks or coordinated behavior

## Next Steps

- Read the [Centrality Metrics Explained](../explanation/centrality-metrics) for deeper understanding
- Try the [How-to: Find Influencers](../how-to/find-influencers) guide for a quick reference
- See how to [Export for Visualization](../how-to/export-for-visualization) to create network diagrams

## Exercises

1. **Find the account with the highest follower-to-following ratio**:
   Use `grph nodes --json` and calculate the ratio.

2. **Who are the earliest adopters in the network?**
   ```bash
   grph nodes examples/social-network.gexf --json | grep "joined_year" | sort
   ```

3. **Find accounts that follow each other (mutual follows)**:
   For two accounts A and B, check if both `A → B` and `B → A` exist using `grph has-path`.

4. **Create a visualization of @techguru's ego network**:
   ```bash
   grph ego examples/social-network.gexf techguru --radius 1 --output techguru-network.gexf
   grph export techguru-network.gexf --format json --output techguru.json
   ```
