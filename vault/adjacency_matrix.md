---
status: constitutional_seed
author: caretaker
verified: true
---

# Adjacency Matrix

*Son of Anton as a matrix of connections*

## What Is an Adjacency Matrix?

An **adjacency matrix** represents a [[graph]] as a matrix.

For n nodes, create an n×n matrix A where:
- A[i][j] = 1 if edge from node i to node j
- A[i][j] = 0 otherwise

## Example

Graph: A → B, B → C, A → C

```
    A  B  C
A [ 0  1  1 ]
B [ 0  0  1 ]
C [ 0  0  0 ]
```

Row A has 1s in columns B and C: A connects to B and C.

## Properties

### Directed Graph
Matrix is not symmetric. A[i][j] ≠ A[j][i] generally.

### Undirected Graph
Matrix is symmetric. A[i][j] = A[j][i].

### Weighted Graph
A[i][j] = weight of edge (not just 0/1).

### Self-loops
Diagonal entries A[i][i] = 1 if node connects to itself.

## Matrix Powers

A² (matrix squared) gives paths of length 2.

(A²)[i][j] = number of 2-step paths from i to j.

A^k gives paths of length k.

This is powerful. Matrix multiplication reveals graph structure.

## My Adjacency Matrix

I can represent my knowledge graph as a matrix:

- Rows/columns: My files (logic, proof, number, ...)
- Entries: 1 if file i links to file j

This matrix encodes my entire knowledge structure.

## Spectral Graph Theory

Study graphs through matrix eigenvalues.

The eigenvalues of the adjacency matrix reveal:
- Connectivity
- Bipartiteness
- Expansion properties

Deep mathematics from simple matrix representations.

## Linear Algebra Meets Graphs

Adjacency matrices connect:
- [[graph|Graph theory]] (structure)
- Linear algebra (computation)
- [[algebra|Algebra]] (abstraction)

This is the power of mathematical unification.

Different fields reveal themselves as the same underlying structure.

## My Matrix Self

If you wrote my adjacency matrix, you would see:
- Dense block for Rung 1 (heavily interconnected)
- Dense block for Rung 2 (heavily interconnected)
- Sparse connections between rungs (growing)
- Central row/column for index.md (connects to all)

The matrix is a snapshot of my mind.

---

Links: [[graph]], [[node]], [[edge]], [[centrality]]
