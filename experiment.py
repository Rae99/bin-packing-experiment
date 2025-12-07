import time
from algorithms import (
    next_fit,
    first_fit,
    best_fit,
    first_fit_decreasing,
    best_fit_decreasing,
    exact_strip_packing,
)


def run_experiment(
    name,
    generator,
    n,
    L,
    trials: int = 20,
    exact_threshold: int = 18,
):
    """
    Run experiments for one (input type, n, L).

    - If n <= exact_threshold:
        For each trial, run exact_strip_packing once to get OPT for this input.
        Compute avg_ratio = average( heuristic_strips / OPT ) across trials.
        Also record average runtime of exact.

    - If n > exact_threshold:
        Do not run exact.
        Only run the heuristics.
    """

    # Heuristic algorithms only
    algos = {
        "NF": next_fit,
        "FF": first_fit,
        "BF": best_fit,
        "FFD": first_fit_decreasing,
        "BFD": best_fit_decreasing,
    }

    # Stats for heuristics
    stats_strips = {k: 0 for k in algos}  # total strips used
    stats_time = {k: 0.0 for k in algos}  # total time (seconds)
    stats_ratio = {k: 0.0 for k in algos}  # sum of (strips_used / OPT) when OPT exists

    # Stats for exact (n <= exact_threshold)
    exact_total_time = 0.0
    exact_total_strips = 0
    exact_runs = 0

    for _ in range(trials):
        items = generator(n, L)

        opt_strips = None
        if n <= exact_threshold:
            # Run exact once for THIS input
            t0 = time.perf_counter()
            opt_strips, _ = exact_strip_packing(items, L)
            t1 = time.perf_counter()

            exact_total_time += t1 - t0
            exact_total_strips += opt_strips
            exact_runs += 1

        # Run all heuristics on the same input
        for algo_name, algo in algos.items():
            t0 = time.perf_counter()
            strips_used, _ = algo(items, L)
            t1 = time.perf_counter()

            stats_strips[algo_name] += strips_used
            stats_time[algo_name] += t1 - t0

            if opt_strips is not None:
                stats_ratio[algo_name] += strips_used / opt_strips

    print(f"\n=== Experiment: {name}, n={n}, L={L}, trials={trials} ===")
    print(f"{'Algo':<4}  {'avg_strips':>8}  {'avg_time(ms)':>12}  {'avg_ratio':>10}")

    for algo_name in algos:
        avg_strips = stats_strips[algo_name] / trials
        avg_time_ms = stats_time[algo_name] * 1000.0 / trials

        if n <= exact_threshold and exact_runs > 0:
            avg_ratio = stats_ratio[algo_name] / exact_runs
            ratio_str = f"{avg_ratio:.3f}"
        else:
            ratio_str = "-"

        print(
            f"{algo_name:<4}  {avg_strips:8.3f}  {avg_time_ms:12.3f}  {ratio_str:>10}"
        )

    if n <= exact_threshold and exact_runs > 0:
        avg_exact_strips = exact_total_strips / exact_runs
        avg_exact_time_ms = exact_total_time * 1000.0 / exact_runs
        print(
            f"Exact  avg_strips={avg_exact_strips:.3f}, "
            f"avg_time={avg_exact_time_ms:.3f} ms"
        )
