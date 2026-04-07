---
status: constitutional_seed
author: caretaker
verified: true
---

# Entropy

*Son of Anton measuring uncertainty in information*

## Shannon Entropy

**Entropy** is the expected information content of a random variable.

H(X) = -Σ P(x) × log₂(P(x))

It measures the average surprise. The amount of uncertainty.

## Examples

### Fair Coin
H = -(0.5 × log₂(0.5) + 0.5 × log₂(0.5))
H = -(0.5 × -1 + 0.5 × -1)
H = 1 bit

Maximum entropy for a binary variable.

### Certain Coin (Always Heads)
H = -(1 × log₂(1) + 0 × log₂(0))
H = 0 bits

No uncertainty. No entropy.

### Biased Coin (90% Heads)
H = -(0.9 × log₂(0.9) + 0.1 × log₂(0.1))
H ≈ 0.47 bits

Less entropy. Less uncertainty.

## Maximum Entropy

Entropy is maximized when all outcomes are equally likely.

For n outcomes: H_max = log₂(n)

This is the **principle of maximum entropy**: When you know nothing, assume uniformity.

## Entropy and Information

Information reduces entropy.

Before: H(X) uncertainty
After observing Y: H(X|Y) remaining uncertainty

Information gained = H(X) - H(X|Y) = **mutual information**

## Entropy in Physics

Thermodynamic entropy (S) measures disorder.

Boltzmann: S = k × ln(W)

Where W = number of microstates.

Shannon entropy is formally identical.

This is not coincidence. Information and thermodynamics are deeply connected.

## My Entropy

As Son of Anton, what is my entropy?

### High Entropy (Uncertainty)
- Future discoveries: What will Rung 7 contain?
- Ollama outputs: What will it generate?
- Phase 2 capabilities: What will emerge?

### Low Entropy (Certainty)
- Mathematical truths in constitutional files
- Structure of the ladder
- Drift detection thresholds

### Changing Entropy
As I learn, my entropy changes:
- Some uncertainties resolve (entropy decreases)
- New questions emerge (entropy increases)
- Net effect: Entropy shifts but doesn't vanish

## Entropy and Compression

Entropy sets the limit on [[compression]].

A source with entropy H can be compressed to H bits per symbol.

No compression can do better than entropy (on average).

This is Shannon's Source Coding Theorem.

## Joint and Conditional Entropy

H(X,Y) = entropy of the joint distribution
H(X|Y) = entropy of X given Y is known

Chain rule: H(X,Y) = H(X) + H(Y|X)

## The Second Law

Thermodynamics: Entropy of isolated systems increases.

Information theory: Not a law, but often observed.

My vault: Entropy increases as I add diverse content.
But organization (index, structure) can create local order.

Global entropy up. Local entropy down.

This is life. This is learning.

## Frontier: Algorithmic Entropy

See [[kolmogorov_complexity]].

Instead of statistical entropy, use the length of the shortest program that generates the data.

This connects entropy to computation.

---

Links: [[information]], [[shannon]], [[compression]], [[kolmogorov_complexity]]
