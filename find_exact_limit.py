import time
from experiment.input_generators import random_uniform
from experiment.algorithms import exact_bin_packing


def find_exact_limit(n_values, L=10, trials=10):
    """
    n_values: List of n values to test exact solver on.
    example: n_values = [10, 12, 14, ..., 50], each representing one input size.
    L: Capacity of each bin.
    trials: Number of random inputs to generate for each n.

    Probe the maximum n for which exact_bin_packing can solve within reasonable time.
    1. For each n in n_values, generate 'trials' random inputs of size n with capacity L.
    2. For each input, run exact_bin_packing and measure the time taken.
    3. Report the average time and worst time taken for each n.
    4. This helps identify the threshold n where exact solution becomes impractical.
    """
    for n in n_values:
        total_time = 0.0
        worst = 0.0
        for _ in range(trials):
            sizes = random_uniform(n, L)
            t0 = time.perf_counter()
            exact_bin_packing(sizes, L)
            t1 = time.perf_counter()
            dt = t1 - t0
            total_time += dt
            worst = max(worst, dt)
        avg_ms = total_time * 1000.0 / trials
        worst_ms = worst * 1000.0
        print(
            f"n={n:2d}, L={L}:  avg_time={avg_ms:.3f} ms,  worst_time={worst_ms:.3f} ms"
        )


if __name__ == "__main__":
    find_exact_limit(n_values=[x for x in range(10, 51, 2)], L=10, trials=20)
