![A Conservative Matrix Field (CMF) contains many celebrated formulas from the literature.](image.png)
*A Conservative Matrix Field (CMF) contains many celebrated formulas from the literature.*

# From Euler to AI: Unifying Formulas for Mathematical Constants

This repository accompanies the research article "[From Euler to AI: Unifying Formulas for Mathematical Constants](https://arxiv.org/abs/2502.17533)".
The paper introduces a systematic methodology for discovering equivalences for formulas representing mathematical constants,
utilizing modern large language models for data collection and innovative mathematical algorithms for proof discovery.
Using this framework, many formulas are found to be embedded in a single mathematical structure termed a Conservative Matrix Field (CMF), which was [recently discovered](https://www.pnas.org/doi/10.1073/pnas.2321440121).
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

Now represented as polynomial recurrences, formulas undergo:  
1. Computation of dynamical metrics: the irrationality measure ($\delta$) and convergence rate are calculated.
2. Initial clustering: based on the $\delta$ metric.
3. Formula matching: new algorithms are applied to discover novel connections between formulas.

The result is a graph, specifically a collection of cliques, containing novel transformations between formulas that prove they are equivalent.

## Getting Started

For a quick intro, please check out the tutorial [notebook](https://colab.research.google.com/drive/13EC9hwEhoA_xvEu_7p_9wbIl2QjDknqC?authuser=1#scrollTo=Jh-CDhaF0twQ).

To reproduce the results and explore the methodologies presented in the paper, follow these steps:

1. **Clone the repository and install the `unifier` package**:
   ```bash
   git clone https://github.com/RamanujanMachine/unifying-formulas-for-math-constants.git
   cd unifying-formulas-for-math-constants
   pip install .
   ```

   or simply

   ```bash
   pip install git+https://github.com/RamanujanMachine/unifying-formulas-for-math-constants.git
   ```
   and then download the relevant data separately.

**Proceed to step 3 if you are interested in recreating the paper's results without testing the harvesting pipeline.**

2. **Harvesting formulas**:  
   The 6-step harvesting pipeline can be found under `dataset.acquisition`.  
   Under this directory, the file `config.py` contains the following settings:
   - `BASE_DIR`: directory in which to store intermediate pipeline results, from each step.
   - `ARXIV_IDS_OF_INTEREST`: a list of arXiv ids to be scraped for formulas (pickle of a list or a list, if #ids is sufficiently small, of id **strings**).  
   - `CONSTANT`: (Note: Only 'pi' is currently supported.) The constant of interest for which formulas should be harvested, as a LaTeX string. 
   - `MAX_WORKERS`: for multiprocessing (configure according to your machine), can only lower the number of workers used throughout the pipeline as the minimum between this and default values are always taken.
   - `OPENAI_API_KEY`: private OpenAI API key.

   Customize `config.py`, then run each of the following scripts in order:
   - `1_scraping.py`: (Note: may take a few weeks for hundreds of thousands of arXiv ids to ensure compliance with the arXiv API guidelines.) Collects LaTeX equation strings from each of the articles in the list `ARXIV_IDS_OF_INTEREST`.  
   - `2_retrieval.py`: Sifts for equations containing series or continued fractions that compute the constant of interest.
   - `3_classification.py`: Classifies each candidate formula as computing the constant of interest or containing the constant's symbol (e.g. $\pi$) in an unrelated context (discarded).
   - `4_extraction.py`: Collects information from LaTeX strings needed to reconstruct and compute the formula in a Computer Algebra System (CAS, SymPy in our case).
   - `5_validation.py`: Computes formulas and finds symbolic values (limits of series and continued fractions) in terms of the constant of interest.
   - `6_to_recurrence.py`: Computes the first 200 terms of each series in preparation for conversion to polynomial recurrences.
   - `6_to_recurrence.wl`: Mathematica code based on [RISC's tool](https://risc.jku.at/sw/guess/) (request access [here](https://www3.risc.jku.at/research/combinat/software/ergosum/installation.html#download)) that finds the correct polynomial-coefficient linear recurrences for, e.g., sequences converging to irrational constants.
   - `6_merge.py`: Collect and organize in a pandas DataFrame all validated formulas (series and continued fractions) yielding polynomial recurrences of order 2, and convert all to canonical forms - polynomial continued fractions (PCFs). (Note: the focus of this study is formulas with order 2 polynomial linear recurrences; we have high hopes for higher-order recurrences in the near future.)  

   This results in a dataframme of formulas in canonical form (PCFs) and their symbolic limits in terms of the constant of interest, along with source metadata.  

3. **Unification**:  
   Scripts for running this section will be found under the directory `unify`. (**NOTE: being refactored**)  
    - The result is a dataframe containing formulas as polynomial continued fractions (PCFs), with their irrationality measures ($\delta$ s) and convergence rates precomputed.
   Using the resulting dataframe, or the one used for the results shown in the paper, `pcfs_dataset/pcfs_10.1.25.pkl`, run `coboundary_graph_all`.
   The resuling graph is a forest in which each tree actually represents a clique (the full cliques are not computed for efficiency).
   Visualize the graph using `plot_connected_components_as_trees` from `coboundary_graph_utils.py`.
   

