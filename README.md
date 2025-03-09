![A Conservative Matrix Field (CMF) contains many celebrated formulas from the literature.](image.png)
*A Conservative Matrix Field (CMF) contains many celebrated formulas from the literature.*

# From Euler to AI: Unifying Formulas for Mathematical Constants

This repository accompanies the research article "[From Euler to AI: Unifying Formulas for Mathematical Constants](https://arxiv.org/abs/2502.17533)".
The paper introduces a systematic methodology for discovering and proving equivalences among formulas representing mathematical constants,
utilizing modern large language models for data collection and innovative mathematical algorithms for proof discovery.
Using this framework, many formulas are found to be embedded in a single mathematical structure termed a Conservative Matrix Field (CMF), which was recently discovered.
The project shows how AI can be paired with tailored algorithms to automatically unify and expand upon mathematical knowledge.

## Overview

There are two main stages to the process: **formula harvesting** (dataset acquisition) and **unification** (proof discovery).

### Formula harvesting

A multi-stage pipeline extracts formulas calculating the constant of interest (e.g. $\pi$) from arXiv papers.

1. Scraping: equations are collected from arXiv papers.
2. Retrieval: equations are scanned for certain regular expressions.
3. Classification: an LLM decides whether each formula calculates the constant of interest, and the classifies the type of formula (series or continued fraction).
4. Extraction: an LLM converts LaTeX to SymPy code which can be used to reconstruct the formulas.
5. Validation: finding the symbolic value of the formula by numerically computing it.
6. Conversion to polynomial recurrences: via RISC's tool (Mathematica).

### Unification

Formulas, now represented as polynomial recurrences, are passed through the following steps

1. Dynamical metric computation: the irrationality measure ($\delta$) and convergence rate are calculated.
2. Initial clustering: based on the above metrics.
3. Formula matching: new algorithms are applied to discover coboundary equivalences between formulas.

The result is a graph, specifically a collection of cliques, containing novel transformations between formulas that prove they are equivalent.

## Getting Started

To reproduce the results and explore the methodologies presented in the paper, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/RamanujanMachine/unifying-formulas-for-math-constants.git
   cd unifying-formulas-for-math-constants
