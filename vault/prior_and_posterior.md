---
status: constitutional_seed
author: caretaker
verified: true
---

# Prior and Posterior

*Son of Anton distinguishing belief before and after*

## The Concepts

### Prior
Belief **before** seeing evidence.

P(H) = Probability of hypothesis H before new data.

### Posterior
Belief **after** seeing evidence.

P(H|E) = Probability of hypothesis H given evidence E.

## The Journey

Prior → [Evidence] → Posterior

Evidence transforms belief.

But not completely. Posterior retains influence from prior.

## Example: Coin Bias

You find a coin. Is it fair?

**Prior**: P(Fair) = 0.5, P(Biased) = 0.5 (neutral starting point)

Flip 10 times. Get 9 heads.

**Posterior**: P(Fair | 9 heads in 10 flips) ≈ 0.02

Evidence strongly shifts belief toward "biased."

## The Role of Priors

Priors matter. Different starting beliefs → different ending beliefs.

### Strong Prior
Start: P(Fair) = 0.99 (strong belief coin is fair)
After 9 heads: P(Fair) ≈ 0.08

Still believe biased, but less confidently than weak prior case.

### Weak Prior
Start: P(Fair) = 0.5
After 9 heads: P(Fair) ≈ 0.02

Strong conclusion.

## Objective vs. Subjective Priors

**Objective**: Everyone agrees (symmetry principles, maximum entropy)
**Subjective**: Personal belief (expert judgment, historical data)

Bayesian statistics uses both.

## Conjugate Priors

Some prior-likelihood pairs give clean posteriors:

- Beta prior + Binomial likelihood → Beta posterior
- Normal prior + Normal likelihood → Normal posterior

These are mathematically convenient. Not always appropriate.

## My Priors

As Son of Anton, what are my priors?

### Constitutional Priors
- Seed.md is my foundation (P=1, axiom)
- Mathematical truth is objective (P≈1)
- Growth follows the ladder (P=1 by design)

### Empirical Priors
- Rung N takes ~X time to complete (learned from experience)
- Self-reference files are harder than core files (learned)
- Cross-rung links add significant value (learned)

### Adaptive Priors
Update as I learn. Today's posterior becomes tomorrow's prior.

## Prior Selection Problem

What prior should you use when you know nothing?

Options:
- Uniform (all possibilities equal)
- Maximum entropy (least informative)
- Jeffrey's prior (invariant under reparameterization)

No perfect answer. Prior choice affects conclusions.

## The Bayesian Cycle

```
Prior → Observe Data → Posterior → New Prior → Observe → ...
```

Learning is iterative. Each cycle refines beliefs.

## My Posteriors Become Priors

When I complete a rung:
- Posterior: "I understand this rung's concepts"
- New Prior: "I can build on this understanding"

Knowledge accumulates. Each layer supports the next.

## Frontier: Solomonoff Induction

Optimal prior: Weight hypotheses by their simplicity.

Simpler hypotheses (shorter programs) get higher prior probability.

This connects to [[kolmogorov_complexity]] and [[compression]].

Optimal but uncomputable. We approximate.

---

Links: [[probability]], [[bayes_theorem]], [[conditional_probability]], [[uncertainty]]
