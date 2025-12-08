import os
import pandas as pd
import matplotlib.pyplot as plt

# Load CSVs
algo_df = pd.read_csv("visualization/algo_results.csv")
solver_df = pd.read_csv("visualization/solver_results.csv")

# Standardize column names for convenience
algo_df.rename(
    columns={
        "dist": "dist",
        "avg_bins": "algo_bins",
        "avg_time_ms": "algo_time",
    },
    inplace=True,
)

solver_df.rename(
    columns={
        "dist": "dist",
        "avg_bins": "opt_bins",
        "avg_time_ms": "solver_time",
    },
    inplace=True,
)

# Merge heuristic & solver results
merged = algo_df.merge(
    solver_df[["dist", "n", "L", "opt_bins", "solver_time"]],
    on=["dist", "n", "L"],
    how="left",
)

# Create output dirs
os.makedirs("visualization/figs/group1_ratio_opt", exist_ok=True)
os.makedirs("visualization/figs/group2_runtime", exist_ok=True)
os.makedirs("visualization/figs/group3_relative_ratio", exist_ok=True)
os.makedirs("visualization/figs/group4_summary", exist_ok=True)


# Graph Group 1: Ratio vs n
def plot_ratio_vs_n():
    heuristics = ["BF", "BFD", "FF", "FFD", "NF"]

    for dist in merged["dist"].unique():
        for L in [10, 100]:

            df = merged[(merged["dist"] == dist) & (merged["L"] == L)]
            if df.empty:
                continue

            # Only keep rows that actually have ratio data (small n where exact was run)
            ratio_df = df[df["avg_ratio"].notna()]
            if ratio_df.empty:
                # Nothing meaningful to plot for this (dist, L)
                continue

            plt.figure(figsize=(8, 5))

            # Plot each heuristic as a line over n (only where ratio exists)
            for algo in heuristics:
                sub = ratio_df[ratio_df["algo"] == algo].sort_values("n")
                if sub.empty:
                    continue
                # Default style
                marker = "o"
                markersize = 6

                # Make BFD marker larger so it doesn't get hidden behind FFD
                if algo == "BFD":
                    markersize = 10

                plt.plot(
                    sub["n"],
                    sub["avg_ratio"],
                    marker=marker,
                    markersize=markersize,
                    label=algo,
                )

            # OPT line (ratio = 1 always), across the n range where ratios exist
            ns = sorted(ratio_df["n"].unique())
            plt.plot(ns, [1.0] * len(ns), "k--", label="OPT")

            plt.title(f"Ratio vs n — {dist}, L={L}")
            plt.xlabel("n")
            plt.ylabel("Average Ratio")

            # Focus y-axis around the actual ratios instead of [0.9, 1.3] blindly
            ymin = min(1.0, ratio_df["avg_ratio"].min()) - 0.02
            ymax = ratio_df["avg_ratio"].max() + 0.05
            plt.ylim(ymin, ymax)

            # Limit x-axis to the n values where we have ratios (small n),
            # plus a small margin so points are not glued to the border.
            xmin = min(ns)
            xmax = max(ns)
            margin = max(1, int(0.1 * (xmax - xmin)))  # small padding in n units
            plt.xlim(xmin - margin, xmax + margin)

            plt.legend()
            plt.grid(alpha=0.3)

            filename = f"visualization/figs/group1_ratio_opt/{dist}_L{L}_ratio_vs_n.png"
            plt.savefig(filename, dpi=200)
            plt.close()


# Graph Group 2: Runtime vs n
def plot_runtime_vs_n():
    heuristics = ["BF", "BFD", "FF", "FFD", "NF"]

    for dist in merged["dist"].unique():
        for L in [10, 100]:

            df = merged[(merged["dist"] == dist) & (merged["L"] == L)]
            if df.empty:
                continue

            plt.figure(figsize=(8, 5))

            # Heuristic runtimes
            for algo in heuristics:
                sub = df[df["algo"] == algo].sort_values("n")
                if sub.empty:
                    continue
                plt.plot(
                    sub["n"],
                    sub["algo_time"],
                    marker="o",
                    label=f"{algo} time",
                )

            # Solver (exact OPT) runtime – only plot if we actually have data
            solver_sub = (
                df.drop_duplicates(subset=["n"])
                .sort_values("n")
                .dropna(subset=["solver_time"])
            )
            if not solver_sub.empty:
                plt.plot(
                    solver_sub["n"],
                    solver_sub["solver_time"],
                    "s--",
                    label="Solver(opt) time",
                )

            plt.yscale("log")
            plt.title(f"Runtime vs n (log scale) — {dist}, L={L}")
            plt.xlabel("n")
            plt.ylabel("Time (ms, log scale)")
            plt.grid(alpha=0.3)
            plt.legend()

            filename = f"visualization/figs/group2_runtime/{dist}_L{L}_runtime_vs_n.png"
            plt.savefig(filename, dpi=200)
            plt.close()


# Graph Group 3: Large-n relative ratio vs n
def plot_large_n_relative_ratio(algo_df: pd.DataFrame):
    """
    Graph Group 3 (large-n): for each (dist, L), plot relative ratios
    for large n (n > 30), where

        relative_ratio = avg_bins(algo) / min_over_heuristics(avg_bins)

    So 1.0 means this heuristic is the best for that
    (dist, L, n), and >1.0 is worse than the best heuristic.
    """

    heuristics = ["BF", "BFD", "FF", "FFD", "NF"]
    out_dir = "visualization/figs/group3_relative_ratio"
    os.makedirs(out_dir, exist_ok=True)

    # Only keep rows where we actually have heuristic bin counts
    df = algo_df.copy()
    df = df[df["algo_bins"].notna()]

    # Loop over each input type and capacity L
    for dist in sorted(df["dist"].unique()):
        for L in sorted(df["L"].unique()):
            sub = df[(df["dist"] == dist) & (df["L"] == L) & (df["n"] > 30)]
            if sub.empty:
                continue

            # For each (dist, L, n), find the best (minimum) algo_bins
            best_bins = (
                sub.groupby(["dist", "L", "n"])["algo_bins"]
                .min()
                .reset_index()
                .rename(columns={"algo_bins": "min_bins"})
            )

            # Merge back so each row knows its baseline
            merged = sub.merge(best_bins, on=["dist", "L", "n"], how="left")
            merged["rel_ratio"] = merged["algo_bins"] / merged["min_bins"]

            plt.figure(figsize=(6, 4))
            ax = plt.gca()

            # Plot each heuristic as a separate line
            for algo in heuristics:
                curve = merged[merged["algo"] == algo].sort_values("n")
                if curve.empty:
                    continue

                # Slightly larger marker for BFD so it does not hide under others
                markersize = 7 if algo == "BFD" else 5
                linewidth = 1.8 if algo == "BFD" else 1.4

                ax.plot(
                    curve["n"],
                    curve["rel_ratio"],
                    marker="o",
                    markersize=markersize,
                    linewidth=linewidth,
                    label=algo,
                )

            # Baseline line: best heuristic has ratio 1.0
            ax.axhline(
                1.0,
                color="black",
                linestyle="--",
                linewidth=1.0,
                label="Best heuristic",
            )

            ax.set_title(f"Relative Ratio vs n (large n) — {dist}, L={L}")
            ax.set_xlabel("n")
            ax.set_ylabel("avg bins / best heuristic")

            # Make the y-axis slightly tight around the data
            ymin = max(0.95, merged["rel_ratio"].min() - 0.02)
            ymax = merged["rel_ratio"].max() + 0.05
            ax.set_ylim(ymin, ymax)

            ax.grid(True, linestyle="--", alpha=0.3)
            ax.legend()

            safe_dist = dist.replace(" ", "_")
            filename = f"{out_dir}/{safe_dist}_L{L}_relative_ratio_vs_n.png"
            plt.savefig(filename, dpi=200)
            plt.close()


# Overall average ratio bar chart (Group 4-1)
def plot_overall_avg_ratio(algo_df: pd.DataFrame):
    heuristics = ["BF", "BFD", "FF", "FFD", "NF"]
    avg_ratios = []

    for h in heuristics:
        sub = algo_df[(algo_df["algo"] == h) & algo_df["avg_ratio"].notna()]
        avg_ratios.append(sub["avg_ratio"].mean())

    plt.figure(figsize=(6, 4))
    bars = plt.bar(heuristics, avg_ratios)

    plt.title("Overall Average Ratio Across All Input Types(n <= 30)")
    plt.ylabel("Average Ratio")

    # Tight y-axis around the ratios (no need to start from 0)
    ymin = min(avg_ratios) - 0.02
    ymax = max(avg_ratios) + 0.05
    plt.ylim(ymin, ymax)

    # Annotate each bar with the ratio (8 decimal places)
    for bar, ratio in zip(bars, avg_ratios):
        x = bar.get_x() + bar.get_width() / 2.0
        y = bar.get_height()
        plt.text(
            x,
            y + 0.005,
            f"{ratio:.8f}",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    filename = "visualization/figs/group4_summary/overall_avg_ratio.png"
    plt.savefig(filename, dpi=200)
    plt.close()


# Overall average ratio bar chart (Group 4-2)
def plot_overall_avg_ratio_vs_best(algo_df: pd.DataFrame, exact_threshold: int = 30):
    """
    Overall average ratio vs the best heuristic on each (dist, n, L),
    focusing on large-n instances where exact OPT is not available.

    For each (dist, n, L):
        best_bins = min over heuristics of avg_bins
        ratio_to_best(h) = avg_bins(h) / best_bins

    We then average ratio_to_best(h) over all such scenarios for each heuristic.
    """

    # Use only large-n instances, we don't run exact solvers for n > 30
    df_large = algo_df[algo_df["n"] > exact_threshold].copy()
    if df_large.empty:
        print("[Group 3b] No large-n rows found; skip ratio-vs-best plot.")
        return

    # Compute ratio to the best heuristic within each (dist, n, L)
    group_cols = ["dist", "n", "L"]
    best_bins = df_large.groupby(group_cols)["algo_bins"].transform("min")
    df_large["ratio_to_best"] = df_large["algo_bins"] / best_bins

    heuristics = ["BF", "BFD", "FF", "FFD", "NF"]
    avg_ratios = []

    for h in heuristics:
        sub = df_large[df_large["algo"] == h]
        if sub.empty:
            avg_ratios.append(float("nan"))
        else:
            avg_ratios.append(sub["ratio_to_best"].mean())

    # Remove NaNs if any heuristic has no data (just in case)
    valid_pairs = [(h, r) for h, r in zip(heuristics, avg_ratios) if not pd.isna(r)]
    if not valid_pairs:
        print("[Group 3b] All ratios are NaN; skip ratio-vs-best plot.")
        return

    labels, avg_ratios = zip(*valid_pairs)

    plt.figure(figsize=(6, 4))
    bars = plt.bar(labels, avg_ratios)

    plt.title("Overall Average Ratio vs Best Heuristic (large n only, n > 30)")
    plt.ylabel("Average Ratio")

    # Tight y-axis around the ratios (they should all be >= 1)
    ymin = min(avg_ratios) - 0.02
    ymax = max(avg_ratios) + 0.05
    plt.ylim(ymin, ymax)

    # Annotate each bar with the ratio (8 decimal places)
    for bar, ratio in zip(bars, avg_ratios):
        x = bar.get_x() + bar.get_width() / 2.0
        y = bar.get_height()
        plt.text(
            x,
            y + 0.005,
            f"{ratio:.8f}",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    filename = "visualization/figs/group4_summary/overall_avg_ratio_vs_best_large_n.png"
    plt.savefig(filename, dpi=200)
    plt.close()


# plot all figures
if __name__ == "__main__":
    plot_ratio_vs_n()
    plot_runtime_vs_n()
    plot_large_n_relative_ratio(merged)
    plot_overall_avg_ratio(merged)
    plot_overall_avg_ratio_vs_best(merged, exact_threshold=30)
    print("All graphs generated!")
