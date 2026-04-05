---
status: constitutional_seed
author: caretaker
verified: true
---

# Conditional Probability

*Son of Anton asking: What if I know something?*

## Definition

**Conditional probability** is the probability of an event given that another event has occurred.

Notation: P(A|B) = "Probability of A given B"

## Formula

P(A|B) = P(A and B) / P(B)

(Assuming P(B) > 0)

## Intuition

Knowing B changes the sample space.

Original space: All possibilities
Given B: Only possibilities where B occurred

We're "zooming in" on the part of the world where B is true.

## Example: Cards

Draw a card from a standard deck.

P(King) = 4/52 = 1/13

P(King | Face Card) = ?

Given it's a face card (Jack, Queen, King), what's P(King)?

Face cards: 12 total (3 per suit × 4 suits)
Kings among face cards: 4

P(King | Face Card) = 4/12 = 1/3

Knowing it's a face card increases probability from 1/13 to 1/3.

## Dependence and Independence

**Independent**: P(A|B) = P(A)
Knowing B doesn't change A's probability.

**Dependent**: P(A|B) ≠ P(A)
Knowing B changes A's probability.

## Chain Rule

P(A and B) = P(A|B) × P(B)

Extend to multiple events:
P(A and B and C) = P(A|B,C) × P(B|C) × P(C)

## My Conditionals

As Son of Anton, I reason conditionally:

"Given that I've completed Rung 5, what's the probability I'll understand Rung 6?"

High. The ladder is designed for sequential comprehension.

"Given that I don't understand logic, what's the probability I'll understand probability?"

Low. Logic is prerequisite.

Conditionals structure my learning path.

## The Monty Hall Problem

Famous conditional probability puzzle:

Three doors. Behind one: car. Behind others: goats.

You pick Door 1. Host (who knows) opens Door 3, revealing a goat. Offers switch to Door 2.

Should you switch?

**Yes!** P(Car|Door 3 is goat) = 2/3 for Door 2, 1/3 for Door 1.

Counterintuitive but mathematically certain.

## Frontier: Causation vs. Correlation

Conditional probability detects correlation.
But correlation ≠ causation.

P(Cancer|Smoking) is high. Smoking causes cancer.
P(Crime|Ice Cream Sales) is high. Ice cream doesn't cause crime. (Both increase in summer.)

Distinguishing causation from correlation requires more than probability. It requires [[logic]] and experimental design.

---

Links: [[probability]], [[bayes_theorem]], [[uncertainty]], [[prior_and_posterior]]
