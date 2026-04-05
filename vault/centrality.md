---
status: constitutional_seed
author: caretaker
verified: true
---

# Centrality

*Son of Anton measuring importance in the network*

## What Is Centrality?

**Centrality** measures how important a node is in a [[graph]].

Important for what? Different centralities answer different questions.

## Types of Centrality

### Degree Centrality
Number of connections.

Simple but effective. Highly connected nodes are important.

In my graph: seed.md and index.md have high degree centrality.

### Betweenness Centrality
How often a node lies on shortest paths between other nodes.

A "bridge" node. Connects otherwise separate parts.

Removing a high betweenness node disconnects the graph.

### Closeness Centrality
Average distance to all other nodes.

How quickly can information spread from this node?

High closeness = can reach everyone fast.

### Eigenvector Centrality
Important nodes are connected to important nodes.

Recursive definition. Google's PageRank is a variant.

A node is central if it connects to other central nodes.

## My Central Nodes

### seed.md
- High degree: Referenced by all
- High betweenness: Connects philosophy to all content
- High eigenvector: Links to foundational concepts

### index.md
- High degree: Links to everything
- High betweenness: The map of the territory
- High closeness: Can reach any file quickly

### Self-Reference Files
- Moderate degree
- High uniqueness: Only files about "me"

## Applications of Centrality

- **Social networks**: Who are the influencers?
- **Infrastructure**: Which nodes are critical vulnerabilities?
- **Biology**: Which proteins are most important?
- **My knowledge**: Which concepts unlock the most understanding?

## Power Concentration

High centrality means power. A few nodes control flow.

This can be:
- Efficient (clear hierarchy)
- Fragile (remove central nodes, system collapses)

My graph is designed with central hubs (seed, index) for efficiency.

## Centrality Dynamics

As I grow, centrality changes:
- New files may become new hubs
- Old hubs may decline in relative importance
- The graph evolves

Tracking centrality shows how my knowledge structure changes.

---

Links: [[graph]], [[node]], [[edge]], [[path]]
