import os
import pandas as pd
import matplotlib.pyplot as plt

# Load CSVs
algo_df = pd.read_csv("visualization/algo_results.csv")
solver_df = pd.read_csv("visualization/solver_results.csv")

# Using manually parsed CSVs to fix any inconsistencies
# algo_df = pd.read_csv("parse_output_to_csv/algo_results_manual.csv")
# solver_df = pd.read_csv("parse_output_to_csv/solver_results_manual.csv")

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
os.makedirs("visualization/figs/group1_ratio", exist_ok=True)
os.makedirs("visualization/figs/group2_runtime", exist_ok=True)
os.makedirs("visualization/figs/group3_summary", exist_ok=True)


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

            filename = f"visualization/figs/group1_ratio/{dist}_L{L}_ratio_vs_n.png"
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


# Overall average ratio bar chart (Group 3)
def plot_overall_avg_ratio(algo_df: pd.DataFrame):
    heuristics = ["BF", "BFD", "FF", "FFD", "NF"]
    avg_ratios = []

    for h in heuristics:
        sub = algo_df[(algo_df["algo"] == h) & algo_df["avg_ratio"].notna()]
        avg_ratios.append(sub["avg_ratio"].mean())

    plt.figure(figsize=(6, 4))
    bars = plt.bar(heuristics, avg_ratios)

    plt.title("Overall Average Ratio Across All Input Types")
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

    filename = "visualization/figs/group3_summary/overall_avg_ratio.png"
    plt.savefig(filename, dpi=200)
    plt.close()


# RUN ALL
if __name__ == "__main__":
    plot_ratio_vs_n()
    plot_runtime_vs_n()
    plot_overall_avg_ratio(merged)
    print("All graphs generated!")
