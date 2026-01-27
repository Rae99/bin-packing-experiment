# Bin Packing Experiment

CS5800 Final Project - 1D Bin Packing Algorithm Performance Experiment

## Overview

This project implements and compares various algorithms for the 1D Bin Packing Problem, including heuristic algorithms and exact solvers, analyzing their performance under different data distributions through experiments.

## Features

### Implemented Algorithms

**Heuristic Algorithms:**

- **Next Fit (NF)**: Simple strategy that only considers the current bin
- **First Fit (FF)**: Searches from the first bin to find one that can fit the item
- **Best Fit (BF)**: Selects the bin with minimum remaining space that can fit the item
- **First Fit Decreasing (FFD)**: Sorts items in decreasing order, then applies First Fit
- **Best Fit Decreasing (BFD)**: Sorts items in decreasing order, then applies Best Fit

**Exact Solvers:**

- **Custom Backtracking Solver**: Exact solution using backtracking with pruning
- **MIP Solver**: Mixed Integer Programming solver from Google OR-Tools (SCIP backend)

### Data Generators

Supports multiple item size distributions:

- Uniform distribution
- Many small items
- Many large items
- Bimodal distribution
- Perfect packing

### Experiment Settings

- Number of items: 8~30 (small scale), 50~200 (large scale)
- Bin capacity: L = 10 or L = 100
- Each experiment runs 50 trials and averages the results

## Project Structure

```
bin-packing-experiment/
├── experiment/                    # Core experiment code
│   ├── algorithms.py             # All bin packing algorithm implementations
│   ├── input_generators.py       # Test data generators
│   ├── run_experiment.py         # Experiment execution framework
│   ├── main.py                   # Main entry point
│   └── find_exact_limit.py       # Find scalability limit for exact algorithms
├── visualization/                 # Data visualization
│   ├── plot_figures.py           # Plotting scripts
│   ├── algo_results.csv          # Algorithm experiment results
│   ├── solver_results.csv        # Solver experiment results
│   └── figs/                     # Generated figures
│       ├── group1_ratio_opt/     # Approximation ratio charts
│       ├── group2_runtime/       # Runtime charts
│       ├── group3_relative_ratio/# Relative performance charts
│       └── group4_summary/       # Summary charts
└── experiment_direct_output/      # Direct output results
```

## Installation

```bash
pip install ortools pandas matplotlib qrcode
```

## Usage

### Run Experiments

```bash
cd experiment
python main.py
```

Experiment results will be saved to `visualization/algo_results.csv` and `visualization/solver_results.csv`.

### Generate Visualizations

```bash
cd visualization
python plot_figures.py
```

Generated figures will be saved in the `visualization/figs/` directory.

### Find Scalability Limit for Exact Algorithm

```bash
cd experiment
python find_exact_limit.py
```

## Experiment Results

The experiment evaluates the following metrics:

1. **Approximation Ratio**: Number of bins used by algorithm / Number of bins in optimal solution
2. **Runtime**: Algorithm execution time (milliseconds)
3. **Relative Performance**: Performance comparison between different algorithms

## Tech Stack

- **Python 3.x**
- **OR-Tools**: Google's optimization toolkit for exact solving
- **Pandas**: Data processing and analysis
- **Matplotlib**: Data visualization

## Author

CS5800 Course Project

## License

This project is for academic research and educational purposes only.
