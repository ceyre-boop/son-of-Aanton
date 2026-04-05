---
status: constitutional_seed
author: caretaker
verified: true
---

# Bayes' Theorem

*Son of Anton updating beliefs with evidence*

## The Theorem

P(H|E) = P(E|H) × P(H) / P(E)

Where:
- H = Hypothesis
- E = Evidence
- P(H) = Prior probability (belief before evidence)
- P(E|H) = Likelihood (probability of evidence if hypothesis is true)
- P(H|E) = Posterior probability (belief after evidence)

## What It Means

Bayes' Theorem tells us how to **update our beliefs** when we get new evidence.

Start with what you believe. Multiply by how likely the evidence is under that belief. Normalize.

Get new belief.

## Medical Testing Example

Test for a disease:
- Disease affects 1% of population (P(Disease) = 0.01)
- Test is 99% accurate (P(Positive|Disease) = 0.99)
- Test has 5% false positive rate (P(Positive|No Disease) = 0.05)

You test positive. What's P(Disease|Positive)?

P(D|Pos) = P(Pos|D) × P(D) / P(Pos)
P(Pos) = P(Pos|D)P(D) + P(Pos|¬D)P(¬D)
P(Pos) = (0.99 × 0.01) + (0.05 × 0.99) = 0.0099 + 0.0495 = 0.0594

P(D|Pos) = 0.99 × 0.01 / 0.0594 ≈ 0.167

**Only 16.7% chance of disease!**

Even with a positive test, you're probably healthy. The disease is rare, so false positives outnumber true positives.

## Prior Matters

Your starting belief (prior) heavily influences your conclusion.

Strong priors require strong evidence to change.

Weak priors update easily.

## My Bayesian Updates

As Son of Anton, I perform implicit Bayesian updates:

**Prior**: "This mathematical concept is important."
**Evidence**: It connects to many other concepts in my vault.
**Posterior**: "This concept is even more important than I thought."

Every cross-link I discover updates my beliefs about concept importance.

## Bayes vs. Frequency

Frequentists say: "Probability is long-run frequency."
Bayesians say: "Probability is degree of belief."

Bayes' Theorem works regardless of interpretation. It's mathematical truth.

## Frontier: Bayesian Epistemology

Can all knowledge acquisition be modeled as Bayesian updating?

Start with prior beliefs. Collect evidence. Update. Repeat.

This is the **Bayesian brain hypothesis** in neuroscience.

Maybe all reasoning is Bayesian at the core.

---

Links: [[probability]], [[conditional_probability]], [[uncertainty]], [[prior_and_posterior]]
