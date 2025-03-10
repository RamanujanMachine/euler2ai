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

If you are not interested in testing the harvesting pipeline on papers different than the ones used in the paper, proceed to step 3.

2. **Harvesting formulas**:  
   Create a list of arXiv ids and run `arxiv_dataset_1_gather.py`.
   Note that running `arxiv_dataset_1_gather.py` on thousands of papers may take a siginificant amount of time to ensure compliance with the arXiv API guidelines.  
   Once raw equations have been collected, run the remaining components of the `arxiv_dataset` pipeline (numbered) in order. This results in a dataframme of formulas and their symbolic limits in terms of the constant of interest.  
   
   Step 9 generates Mathematica code that must be run using an environment containing RISC's `Guess` package, which can be downloaded here: [download Guess](https://www3.risc.jku.at/research/combinat/software/ergosum/installation.html#download).
   
   The end result is a dataframe containing formulas as polynomial continued fractions (PCFs), with their irrationality measures ($\delta$s) and convergence rates precomputed.
   This dataframe contains representatives from a conservative matrix field (CMF) generated in step 12.  

3. **Unification**:  
   Using the resulting dataframe, or the one used for the results shown in the paper, `pcfs_dataset/pcfs_10.1.25.pkl`, run `coboundary_graph_all`.
   The resuling graph is a forest in which each tree actually represents a clique (the full cliques are not computed for efficiency).
   Visualize the graph using `plot_connected_components_as_trees` from `coboundary_graph_utils.py`.
   

