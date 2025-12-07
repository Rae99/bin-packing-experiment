import time
from experiment.algorithms import (
    next_fit,
    first_fit,
    best_fit,
    first_fit_decreasing,
    best_fit_decreasing,
    exact_bin_packing,
    mip_bin_packing,
)


def run_experiment(
    name,
    generator,
    n,
    L,
    trials: int = 20,
    exact_threshold: int = 30,
    mip_threshold: int = 12,
):
    """
    Run experiments for one (input type, n, L).

    - If n <= exact_threshold:
        For each trial, run exact solvers once to get OPT for this input.
        OPT is taken as the minimum number of bins among:
            my_own_exact_solver (recursive exact)
            MIP (OR-Tools MIP baseline, only if n <= mip_threshold)
        We always check whether my_own_exact_solver and MIP agree when both are run.
        Compute avg_ratio = average( heuristic_bins / OPT ) across trials.
        Also record average runtime of each exact solver.

    - If n > exact_threshold:
        Do not run exact.
        Only run the heuristics.
    """

    # Heuristic algorithms only
    heuristics_algos = {
        "NF": next_fit,
        "FF": first_fit,
        "BF": best_fit,
        "FFD": first_fit_decreasing,
        "BFD": best_fit_decreasing,
    }

    # Exact solvers
    # Always run my_own_exact_solver as the exact baseline.
    exact_solvers = {
        "my_own_exact_solver": exact_bin_packing,
    }
    # Only add MIP when n is small enough (n <= mip_threshold)
    if n <= mip_threshold:
        exact_solvers["MIP"] = mip_bin_packing

    # Stats for heuristics
    stats_bins = {k: 0 for k in heuristics_algos}  # total bins used
    stats_time = {k: 0.0 for k in heuristics_algos}  # total time (seconds)
    stats_ratio = {
        k: 0.0 for k in heuristics_algos
    }  # sum of (bins_used / OPT) when OPT exists

    # Stats for each exact solver
    exact_stats_bins = {k: 0 for k in exact_solvers}  # total bins used
    exact_stats_time = {k: 0.0 for k in exact_solvers}  # total time (seconds)

    # For reporting average OPT (min over exact solvers per trial)
    opt_total_bins = 0
    opt_runs = 0

    # Count mismatches between my_own_exact_solver and MIP
    exact_mismatch_count = 0

    for _ in range(trials):
        items = generator(n, L)

        opt_bins = None

        if n <= exact_threshold:
            # Run exact solutions once for THIS input
            per_input_bins = {}
            per_input_time = {}

            for solver_name, solver in exact_solvers.items():
                t0 = time.perf_counter()
                solver_bins, _ = solver(items, L)
                t1 = time.perf_counter()

                # accumulate stats for this exact solver
                exact_stats_bins[solver_name] += solver_bins
                exact_stats_time[solver_name] += t1 - t0

                # per-input record
                per_input_bins[solver_name] = solver_bins
                per_input_time[solver_name] = t1 - t0

                # update OPT for this input
                if opt_bins is None or solver_bins < opt_bins:
                    opt_bins = solver_bins

            # check if two exact solvers agree on this input
            if "my_own_exact_solver" in per_input_bins and "MIP" in per_input_bins:
                n_my = per_input_bins["my_own_exact_solver"]
                n_mip = per_input_bins["MIP"]
                if n_my != n_mip:
                    exact_mismatch_count += 1
                    print(
                        f"[MISMATCH] my_own_exact_solver={n_my}, "
                        f"MIP={n_mip}, items={items}"
                    )

                # print(
                #     f"[Exact vs MIP time] my_own={per_input_time['my_own_exact_solver']*1000:.2f}ms, "
                #     f"MIP={per_input_time['MIP']*1000:.2f}ms"
                # )

            opt_total_bins += opt_bins
            opt_runs += 1

        # Run all heuristics on the same input
        for algo_name, algo in heuristics_algos.items():
            t0 = time.perf_counter()
            bins_used, _ = algo(items, L)
            t1 = time.perf_counter()

            stats_bins[algo_name] += bins_used
            stats_time[algo_name] += t1 - t0

            if opt_bins is not None:
                stats_ratio[algo_name] += bins_used / opt_bins

    print(f"\n=== Experiment: {name}, n={n}, L={L}, trials={trials} ===")
    print(f"{'Algo':<10} {'avg_bins':>10} {'avg_time(ms)':>14} {'avg_ratio':>10}")

    # Heuristics summary
    for algo_name in heuristics_algos:
        avg_bins = stats_bins[algo_name] / trials
        avg_time_ms = stats_time[algo_name] * 1000.0 / trials

        if n <= exact_threshold and opt_runs > 0:
            avg_ratio = stats_ratio[algo_name] / opt_runs
            ratio_str = f"{avg_ratio:.8f}"
        else:
            ratio_str = "-"

        print(f"{algo_name:<10} {avg_bins:10.8f} {avg_time_ms:14.3f} {ratio_str:>10}")

    # Exact solvers summary
    if n <= exact_threshold and opt_runs > 0:
        print("\nExact solvers:")
        print(f"{'Solver':<20} {'avg_bins':>10} {'avg_time(ms)':>14}")

        for solver_name in exact_solvers:
            avg_exact_bins = exact_stats_bins[solver_name] / trials
            avg_exact_time_ms = exact_stats_time[solver_name] * 1000.0 / trials
            print(f"{solver_name:<20} {avg_exact_bins:10.8f} {avg_exact_time_ms:14.3f}")

        avg_opt = opt_total_bins / opt_runs
        print(f"\nEstimated OPT (min over exact solvers) avg_bins = {avg_opt:.8f}")

        if "MIP" in exact_solvers:
            if exact_mismatch_count == 0:
                print("my_own_exact_solver vs MIP: all trials matched in #bins")
            else:
                print(f"my_own_exact_solver vs MIP: {exact_mismatch_count} mismatches")
