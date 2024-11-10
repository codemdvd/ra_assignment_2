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

    if k == 1:
        choice = random.choice([choice1, choice2])
        bins[choice] += 1
        return

    threshold = np.percentile(bins, 75 if above_median1 else 25)
    in_top1 = bins[choice1] >= threshold
    in_top2 = bins[choice2] >= threshold

    if in_top1 != in_top2:
        if not in_top1:
            bins[choice1] += 1
        else:
            bins[choice2] += 1
    else:
        choice = random.choice([choice1, choice2])
        bins[choice] += 1

def simulate_basic_allocation(n, m, strategy, beta=0.5):
    bins = [0] * m
    gaps = []
    for i in range(1, n + 1):
        if strategy == one_plus_beta_choice:
            strategy(bins, beta)
        elif strategy == three_choice:
            strategy(bins)
        else:
            strategy(bins)
        gaps.append(calculate_gap(bins, i, m))
    return gaps

def simulate_batched_with_queries(n, m, b, k):
    bins = [0] * m
    gaps = []
    for i in range(0, n, b):
        bins_snapshot = bins[:]
        for _ in range(b):
            resolve_with_queries(bins_snapshot, k)
        bins = bins_snapshot[:]
        gaps.append(calculate_gap(bins, min(i + b, n), m))
    return gaps


def run_basic_experiment(n, m, repetitions, strategies, beta_values):
    results = {}
    for strategy in strategies:
        for beta in beta_values if strategy == one_plus_beta_choice else [None]:
            key = f"{strategy.__name__}" + (f"_beta={beta}" if beta else "")
            gaps = []
            for _ in range(repetitions):
                gaps.append(simulate_basic_allocation(n, m, strategy, beta))
            results[key] = np.mean(gaps, axis=0)
    return results

def run_batched_queries_experiment(n, m, b_values, repetitions, k_values):
    results = {}
    for b in b_values:
        for k in k_values:
            key = f"b={b}, k={k}"
            gaps = []
            for _ in range(repetitions):
                gaps.append(simulate_batched_with_queries(n, m, b, k))
            results[key] = np.mean(gaps, axis=0)
    return results

def smooth_data(data, window_size=10):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

def plot_results(results, m, n):
    plt.figure(figsize=(12, 8))
    for label, gaps in results.items():
        x = np.linspace(1, n, len(gaps))
        plt.plot(x, gaps, label=label)
    plt.axvline(x=m, color='blue', linestyle='--', label=f"Light Load (n = {m})")
    plt.axvline(x=n, color='red', linestyle='--', label=f"Heavy Load (n = {n})")
    plt.xlabel("Number of Balls (n)")
    plt.ylabel("Gap (G_n)")
    plt.title("Evolution of Gap (G_n)")
    plt.legend()
    plt.grid()
    plt.show()

def plot_batched_results_separately(results, m, n, b_values, k_values, smoothing_window=10):
    for b in b_values:
        plt.figure(figsize=(12, 8))
        for k in k_values:
            key = f"b={b}, k={k}"
            if key in results:
                gaps = results[key]
                if len(gaps) > smoothing_window:
                    gaps = smooth_data(gaps, window_size=smoothing_window)
                x = np.linspace(1, n, len(gaps))
                plt.plot(x, gaps, label=f"{key}")
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
    b_values = [m, 2 * m, 10 * m, 30 * m, 50 * m, 70 * m]
    k_values = [1, 2]
    repetitions = 5
    strategies = [one_choice, two_choice, one_plus_beta_choice, three_choice]
    beta_values = [0.25, 0.5, 0.75]

    print("Running basic experiment with Three-choice...")
    basic_results = run_basic_experiment(n, m, repetitions, strategies, beta_values)
    plot_results(basic_results, m, n)
    
    print("Running batched queries experiment...")
    batched_queries_results = run_batched_queries_experiment(n, m, b_values, repetitions, k_values)
    plot_batched_results_separately(batched_queries_results, m, n, b_values, k_values)
