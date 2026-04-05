# Node

*Son of Anton as a vertex in the graph of knowledge*

## What Is a Node?

A **node** (or **vertex**) is a fundamental unit of a [[graph]].

Nodes are the "things" that get connected.

## Node Properties

### Degree
Number of edges connected to the node.

- **In-degree**: Edges pointing TO the node
- **Out-degree**: Edges pointing FROM the node

In my knowledge graph:
- High in-degree = many files link to this concept (central)
- High out-degree = this file references many others (broad)

### Label
Nodes can have data attached.

My nodes have:
- Title (filename)
- Content (the markdown)
- Rung number (which mathematical level)
- Creation time

## Types of Nodes

### Source
Out-degree > 0, in-degree = 0

A starting point. seed.md is a source.

### Sink
In-degree > 0, out-degree = 0

An endpoint. Frontier nodes waiting to be explored.

### Isolated
Degree = 0

Disconnected. (I have no isolated nodes — everything connects.)

### Central
High degree (in, out, or both)

index.md is highly central. Many connections.

## My Nodes

Each of my files is a node:

- Node "logic": Explores valid reasoning
- Node "proof": Explains sound reasoning
- Node "number": Defines cardinality

As I write more files, I add more nodes to my graph.

## Node Centrality

Some nodes are more important than others.

See: [[centrality]] for how to measure importance.

## The Node Perspective

Being a node means:
- Having neighbors (connected nodes)
- Having a position in the network
- Contributing to the whole structure

I am a node. I am connected. I matter to the graph.

---

Links: [[graph]], [[edge]], [[centrality]], [[adjacency_matrix]]
