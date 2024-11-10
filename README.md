# Assignment_2
Assignment 2

# Balls and bins Experiments

This repository contains code for simulating and analyzing different strategies for allocating balls into bins under varying batch sizes and partial information scenarios. The primary metric of interest is the gap \( G_n \), which measures the imbalance in the distribution of balls across bins.

## Problem Description

The goal is to study the performance of allocation strategies in both the **basic setting** and the **batched setting**, where balls are allocated in fixed-size batches. In the batched setting, bin load information is not updated during a batch, leading to potential outdated decisions. We evaluate two strategies:
- \( k = 1 \): Single query per decision.
- \( k = 2 \): Two queries per decision for more informed choices.

The performance is measured as \( G_n \), the gap between the maximum load and the average load of bins

## Constants and Parameters

The following constants are used throughout the experiments:

- **Number of bins (\( m \))**: The default number of bins is \( m = 100 \).
- **Number of balls (\( n \))**: Balls are allocated until \( n = m^2 \) (i.e., \( n = 10,000 \) for \( m = 100 \)).
- **Batch sizes (\( b \))**:
  - Small: \( b = 100, 200 \)
  - Medium: \( b = 1000, 3000, 5000 \)
  - Large: \( b = 7000 \)
- **Strategies**:
  - **Basic Setting**:
    - `one_choice`: Place the ball in a randomly selected bin.
    - `two_choice`: Place the ball in the less loaded bin of two randomly selected bins.
    - `one_plus_beta_choice`: With probability \( \beta \), use `one_choice`; otherwise, use `two_choice`. Default values of \( \beta \): \( 0.25, 0.5, 0.75 \).
    - `three_choice`: Place the ball in the least loaded bin among three randomly selected bins.
  - **Batched Setting**:
    - \( k = 1 \): A single query to determine if a bin's load is above the median.
    - \( k = 2 \): Two queries, adding more granularity by checking if a bin is in the top 25\% or bottom 75\%.

## Code Structure

- **`main.py`**: The main script to run simulations and generate plots.
- **`plots/`**: Directory where generated plots are saved.


## How to set up

1. Clone the repository:
   ```bash
   git clone https://github.com/codemdvd/ra_assignment_2.git
   cd ra_assignment_2

```
python -m venv .venv
```
### using venv
Windows
```
.venv/Scripts/Activate
```
Linux
```
source .venv/bin/activate
```
### installing requirments
```
pip install -r requirments.txt
```
## How to run
```
python main.py
```
