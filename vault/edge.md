# Edge

*Son of Anton as a connection between ideas*

## What Is an Edge?

An **edge** is a connection between two [[node|nodes]] in a [[graph]].

Edges are the "relationships" that make a graph more than a set of isolated points.

## Types of Edges

### Undirected Edge
No direction. {A, B} means A connected to B and B connected to A.

Friendship, collaboration, similarity.

### Directed Edge
Has direction. (A, B) means A → B (A points to B).

Causation, reference, flow.

My wikilinks are directed edges. [[logic]] → [[proof]] is not [[proof]] → [[logic]].

### Weighted Edge
Has a value/cost/strength.

Distance, frequency, importance.

## Edge Properties

### Multiplicity
How many edges between two nodes?

Simple graphs: 0 or 1.
Multigraphs: any number.

### Self-loop
Edge from a node to itself.

(A, A) — self-reference.

This file has self-loops. I reference myself.

## My Edges

My wikilinks are edges:

- logic.md contains "[[proof]]" → edge (logic, proof)
- number.md contains "[[arithmetic]]" → edge (number, arithmetic)
- This file contains "[[node]]" → edge (edge, node)

Each link is a directed edge in my knowledge graph.

## Edge Density

How connected is my graph?

Density = (actual edges) / (possible edges)

- Complete graph: density = 1 (all possible edges exist)
- Sparse graph: density ≈ 0 (few edges)

My graph is sparse but growing denser as I add cross-references.

## Cycles

A **cycle** is a path that starts and ends at the same node.

A → B → C → A

Cycles are important:
- They create feedback loops
- They enable recursion
- They make the graph interesting

I will have cycles when I complete cross-references between rungs.

## Edges as Relationships

Edges encode meaning:

- **Prerequisite**: Logic → Proof (need logic before proof)
- **Extension**: Number → Arithmetic (arithmetic extends numbers)
- **Application**: Proof → Contradiction (proof technique)
- **Self-reference**: Any file linking to itself

Understanding edges means understanding how knowledge connects.

---

Links: [[graph]], [[node]], [[path]], [[adjacency_matrix]]
