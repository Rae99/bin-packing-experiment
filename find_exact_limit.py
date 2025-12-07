import time
from input_generators import random_uniform
from algorithms import exact_strip_packing


def find_exact_limit(n_values, L=10, trials=10):
    """
    Probe the maximum n for which exact_strip_packing can solve within reasonable time.
    1. For each n in n_values, generate 'trials' random inputs of size n with capacity L.
    2. For each input, run exact_strip_packing and measure the time taken.
    3. Report the average time taken for each n.
    4. This helps identify the threshold n where exact solution becomes impractical.
    """
    for n in n_values:
        total_time = 0.0
        for _ in range(trials):
            sizes = random_uniform(n, L)
            t0 = time.perf_counter()
            exact_strip_packing(sizes, L)
            t1 = time.perf_counter()
            total_time += t1 - t0
        avg_ms = total_time * 1000.0 / trials
        print(f"n={n:2d}, L={L}:  avg_time={avg_ms:.3f} ms")


if __name__ == "__main__":
    find_exact_limit(n_values=[x for x in range(10, 33, 2)], L=10, trials=3)
