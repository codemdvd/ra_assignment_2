# Assignment_2
Assignment 2

# Ball Allocation Strategies: Empirical Study

This repository contains an implementation and empirical study of various strategies for allocating balls into bins under different scenarios. The experiments aim to analyze the effectiveness of these strategies in minimizing the **gap** (\( G_n \)), defined as the difference between the maximum load and the average load of the bins.

## Experiments Overview

### 1. **Basic Experiment**
This experiment evaluates the performance of different allocation strategies when balls are placed into bins sequentially. The tested strategies include:
- **One-Choice**: A single bin is chosen uniformly at random.
- **Two-Choice**: Two bins are chosen randomly, and the ball is placed in the one with the least load.
- **(1+\(\beta\))-Choice**: With probability \(\beta\), one-choice is used; otherwise, two-choice is applied. The study uses \(\beta = 0.25, 0.5, 0.75\).
- **Three-Choice**: Three bins are chosen randomly, and the ball is placed in the one with the least load.

**Goal**: Analyze the evolution of \( G_n \) as the number of balls increases, highlighting the light-load (\( n = m \)) and heavy-load (\( n = m^2 \)) scenarios.

---

### 2. **Batch Allocation Experiment**
In this experiment, balls arrive in batches of size \( b \), and the allocation strategies are applied based on the bin loads at the beginning of each batch. The tested batch sizes include \( b = 100, 200, 1000, 3000, 5000, 7000 \).

**Goal**: Evaluate how delayed information about bin loads affects the strategies and analyze the evolution of \( G_n \) for each batch size.

---

### 3. **Binary Queries Experiment**
This experiment investigates scenarios where only partial information about bin loads is available. Binary queries are used to decide the allocation:
- **\( k = 1 \)**: A query checks if the load of a bin is above the median.
- **\( k = 2 \)**: Additional queries check whether the load is among the top 25\% or bottom 75\%.

The same strategies from the first experiment are tested, with binary queries guiding the allocation decisions.

**Goal**: Assess the impact of limited information and query-based decision-making on minimizing \( G_n \).

---

## Results

- **Basic Experiment**: Three-choice consistently achieves the smallest \( G_n \), followed by two-choice and (1+\(\beta\))-choice with low \(\beta\). One-choice exhibits the largest gap.
- **Batch Allocation Experiment**: Larger batch sizes lead to delayed load updates, increasing \( G_n \). However, multi-choice strategies remain robust.
- **Binary Queries Experiment**: Queries effectively reduce \( G_n \), with \( k = 2 \) marginally outperforming \( k = 1 \). Three-choice benefits the most from query-based decision-making.

---

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
