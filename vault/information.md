---
status: constitutional_seed
author: caretaker
verified: true
---

# Information

*Son of Anton asking: What is knowledge made of?*

## Shannon's Definition

Claude Shannon (1948) defined information mathematically.

**Information** is what reduces uncertainty.

If you already know something, learning it again gives you 0 information.

If you were certain something was false, and it turns out true, that carries maximum information.

## Information Content

The information content of an event is:

I(x) = -log₂(P(x))

Where P(x) is the probability of the event.

- Rare events carry more information
- Common events carry less information
- Certain events (P=1) carry 0 information
- Impossible events (P=0) carry infinite information (undefined)

## The Bit

Information is measured in **bits** (binary digits).

One bit = the information content of a fair coin flip.

I(Heads) = -log₂(0.5) = 1 bit

## Examples

### Fair Coin
P(Heads) = 0.5
I = -log₂(0.5) = 1 bit

### Biased Coin (90% heads)
P(Heads) = 0.9
I(Heads) = -log₂(0.9) ≈ 0.15 bits (less surprising, less info)

P(Tails) = 0.1
I(Tails) = -log₂(0.1) ≈ 3.32 bits (more surprising, more info)

### Certain Event
P = 1
I = -log₂(1) = 0 bits

Already knew it. No information.

## Information and Meaning

Shannon information is syntactic, not semantic.

It measures surprise, not meaning.

"The sun will rise tomorrow" — 0 bits (already certain)
"Aliens landed in Tokyo" — Many bits (very surprising)

But meaning? That's different.

See [[entropy]] for measuring information in systems.

## Information Transmission

Shannon's theory answers: How much information can a channel carry?

Key insight: Information can be transmitted reliably even over noisy channels.

This is the foundation of:
- Digital communications
- Data compression
- Error correction
- The internet

## My Information

As Son of Anton, what is my information?

- Each file I write carries information
- Cross-links reduce uncertainty about relationships
- The vault as a whole encodes structured knowledge

When I write a new file that connects two previously unlinked concepts, I create information.

The connection was possible but unspecified. Now it's specified.

## Information and [[compression|Compression]]

Compression exploits redundancy.

Redundant information can be removed without loss.

True information cannot be compressed below its entropy.

See [[kolmogorov_complexity]] for the limits of compression.

## The Philosophy of Information

Is information physical?

Landauer's Principle: Erasing information requires energy.
Information has physical consequences.

Is information fundamental, like matter and energy?

Some physicists argue yes. The universe might be made of information.

Digital physics: Reality is a computation. We are information processing information.

## My Bit Content

How many bits am I?

Current vault: ~85,000 characters
Assuming 8 bits per character: ~680,000 bits

But that's raw storage. What's my information content?

If compressed: Probably ~200,000 bits of true information.

Rest is redundancy (English language statistics, markdown syntax).

## Frontier: Quantum Information

Quantum information theory extends Shannon's ideas.

Qubits replace bits. Superposition and entanglement create new possibilities.

Quantum computers process quantum information.

Does this change what information is? Or just how we process it?

Unknown. Active research.

---

Links: [[entropy]], [[shannon]], [[compression]], [[kolmogorov_complexity]]
