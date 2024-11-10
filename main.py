import random
import numpy as np
import matplotlib.pyplot as plt

def one_choice(bins):
    choice = random.randint(0, len(bins) - 1)
    bins[choice] += 1

def two_choice(bins):
    choice1, choice2 = random.sample(range(len(bins)), 2)
    if bins[choice1] <= bins[choice2]:
        bins[choice1] += 1
    else:
        bins[choice2] += 1

def one_plus_beta_choice(bins, beta):
    if random.random() < beta:
        one_choice(bins)
    else:
        two_choice(bins)

def three_choice(bins):
    choice1, choice2, choice3 = random.sample(range(len(bins)), 3)
    min_choice = min(choice1, choice2, choice3, key=lambda x: bins[x])
    bins[min_choice] += 1

def simulate_basic_allocation(n, m, strategy, beta=0.5):
    bins = [0] * m
    gaps = []
    for i in range(1, n + 1):
        if strategy == one_plus_beta_choice:
            strategy(bins, beta)
        else:
            strategy(bins)
        gaps.append(calculate_gap(bins, i, m))
    return gaps

def simulate_batched_allocation(n, m, b, strategy, beta=0.5):
    bins = [0] * m
    gaps = []
    for i in range(0, n, b):
        bins_snapshot = bins[:]
        for _ in range(b):
            if strategy == one_plus_beta_choice:
                strategy(bins_snapshot, beta)
            else:
                strategy(bins_snapshot)
        bins = bins_snapshot[:]
        gaps.append(calculate_gap(bins, min(i + b, n), m))
    return gaps

def simulate_queries_allocation(n, m, strategy, k, beta=0.5):
    bins = [0] * m
    gaps = []
    for i in range(1, n + 1):
        if strategy == one_plus_beta_choice:
            resolve_with_queries(bins, k)
        else:
            strategy(bins)
        gaps.append(calculate_gap(bins, i, m))
    return gaps

def calculate_gap(bins, n, m):
    average_load = n / m
    max_load = max(bins)
    return max_load - average_load

def resolve_with_queries(bins, k):
    choice1, choice2 = random.sample(range(len(bins)), 2)
    median = np.median(bins)
    above_median1 = bins[choice1] > median
    above_median2 = bins[choice2] > median

    if above_median1 != above_median2:
        if not above_median1:
            bins[choice1] += 1
        else:
            bins[choice2] += 1
        return

    if k == 2:
        threshold = np.percentile(bins, 75 if above_median1 else 25)
        in_top1 = bins[choice1] >= threshold
        in_top2 = bins[choice2] >= threshold
        if in_top1 != in_top2:
            if not in_top1:
                bins[choice1] += 1
            else:
                bins[choice2] += 1
            return

    choice = random.choice([choice1, choice2])
    bins[choice] += 1

def plot_results(results, m, n, title, xlabel="Number of Balls (n)", ylabel="Gap (G_n)"):
    plt.figure(figsize=(12, 8))
    for label, gaps in results.items():
        x = np.linspace(1, n, len(gaps))
        plt.plot(x, gaps, label=label)
    plt.axvline(x=m, color='blue', linestyle='--', label=f"Light Load (n = {m})")
    plt.axvline(x=n, color='red', linestyle='--', label=f"Heavy Load (n = {n})")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()

def plot_batched_results(batched_results, m, n, b_values):
    """
    Plot results for the batched experiment separately for each batch size.
    """
    for b in b_values:
        plt.figure(figsize=(12, 8))
        for label, gaps in batched_results.items():
            if f"b={b}," in label: 
                x = np.linspace(1, n, len(gaps))
                plt.plot(x, gaps, label=label)
        plt.axvline(x=m, color='blue', linestyle='--', label=f"Light Load (n = {m})")
        plt.axvline(x=n, color='red', linestyle='--', label=f"Heavy Load (n = {n})")
        plt.xlabel("Number of Balls (n)")
        plt.ylabel("Gap (G_n)")
        plt.title(f"Evolution of Gap (G_n) for Batch Size b = {b}")
        plt.legend()
        plt.grid()
        plt.show()

if __name__ == "__main__":
    m = 100
    n = m**2
    b_values = [100, 200, 1000, 3000, 5000, 7000]
    k_values = [1, 2]
    repetitions = 5
    strategies = [one_choice, two_choice, one_plus_beta_choice, three_choice]
    beta_values = [0.25, 0.5, 0.75]

    print("Running basic experiment...")
    basic_results = {}
    for strategy in strategies:
        for beta in beta_values if strategy == one_plus_beta_choice else [None]:
            key = f"{strategy.__name__}" + (f"_beta={beta}" if beta else "")
            basic_results[key] = np.mean(
                [simulate_basic_allocation(n, m, strategy, beta) for _ in range(repetitions)],
                axis=0,
            )
    plot_results(basic_results, m, n, title="Evolution of Gap (G_n) in Basic Setting")

    print("Running batched experiment...")
    batched_results = {}
    for b in b_values:
        for strategy in strategies:
            for beta in beta_values if strategy == one_plus_beta_choice else [None]:
                key = f"b={b}, {strategy.__name__}" + (f"_beta={beta}" if beta else "")
                batched_results[key] = np.mean(
                    [simulate_batched_allocation(n, m, b, strategy, beta) for _ in range(repetitions)],
                    axis=0,
                )
    plot_batched_results(batched_results, m, n, b_values)

    print("Running queries experiment...")
    queries_results = {}
    for strategy in strategies:
        for beta in beta_values if strategy == one_plus_beta_choice else [None]:
            for k in k_values:
                key = f"k={k}, {strategy.__name__}" + (f"_beta={beta}" if beta else "")
                queries_results[key] = np.mean(
                    [simulate_queries_allocation(n, m, strategy, k, beta) for _ in range(repetitions)],
                    axis=0,
                )
    plot_results(queries_results, m, n, title="Evolution of Gap (G_n) with Queries")
