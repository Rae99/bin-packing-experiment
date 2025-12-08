import os
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# Load CSV
# =========================
algo_df = pd.read_csv("parse_output_to_csv/algo_results.csv")
solver_df = pd.read_csv("parse_output_to_csv/solver_results.csv")

# Standardize column names for convenience
algo_df.rename(columns={
    "dist": "dist",
    "avg_bins": "algo_bins",
    "avg_time_ms": "algo_time",
}, inplace=True)

solver_df.rename(columns={
    "dist": "dist",
    "avg_bins": "opt_bins",
    "avg_time_ms": "solver_time",
}, inplace=True)

# Merge heuristic & solver results
merged = algo_df.merge(
    solver_df[["dist","n","L","opt_bins","solver_time"]],
    on=["dist","n","L"],
    how="left"
)

# Create output dirs
os.makedirs("visualization/figs/group1_ratio", exist_ok=True)
os.makedirs("visualization/figs/group2_runtime", exist_ok=True)
os.makedirs("visualization/figs/group3_summary", exist_ok=True)

# =========================
# Graph Group 1: Ratio vs n
# =========================
def plot_ratio_vs_n():
    heuristics = ["BF", "BFD", "FF", "FFD", "NF"]

    for dist in merged["dist"].unique():
        for L in [10, 100]:

            df = merged[(merged["dist"] == dist) & (merged["L"] == L)]
            if df.empty:
                continue

            plt.figure(figsize=(8,5))

            for algo in heuristics:
                sub = df[df["algo"] == algo]
                if not sub.empty:
                    plt.plot(sub["n"], sub["avg_ratio"], marker="o", label=algo)

            # OPT line (ratio = 1 always)
            ns = sorted(df["n"].unique())
            plt.plot(ns, [1]*len(ns), "k--", label="OPT")

            plt.title(f"Ratio vs n — {dist}, L={L}")
            plt.xlabel("n")
            plt.ylabel("Average Ratio")
            plt.ylim(0.9, 1.3)
            plt.legend()
            plt.grid(alpha=0.3)

            filename = f"visualization/figs/group1_ratio/{dist}_L{L}_ratio_vs_n.png"
            plt.savefig(filename, dpi=200)
            plt.close()
            print("Saved:", filename)


# =========================
# Graph Group 2: Runtime vs n
# =========================
def plot_runtime_vs_n():
    heuristics = ["BF", "BFD", "FF", "FFD", "NF"]

    for dist in merged["dist"].unique():
        for L in [10, 100]:

            df = merged[(merged["dist"] == dist) & (merged["L"] == L)]
            if df.empty:
                continue

            plt.figure(figsize=(8,5))

            # Heuristic runtime
            for algo in heuristics:
                sub = df[df["algo"] == algo]
                if not sub.empty:
                    plt.plot(sub["n"], sub["algo_time"], marker="o", label=f"{algo} time")

            # Solver time
            solver_sub = df.drop_duplicates(subset=["n"])
            plt.plot(solver_sub["n"], solver_sub["solver_time"],
                     marker="s", label="Solver(opt) time", linestyle="--")

            plt.yscale("log")
            plt.title(f"Runtime vs n (log scale) — {dist}, L={L}")
            plt.xlabel("n")
            plt.ylabel("Time (ms, log scale)")
            plt.grid(alpha=0.3)
            plt.legend()

            filename = f"visualization/figs/group2_runtime/{dist}_L{L}_runtime_vs_n.png"
            plt.savefig(filename, dpi=200)
            plt.close()
            print("Saved:", filename)


# =========================
# Graph Group 3: Summary bar chart
# =========================
def plot_global_avg_ratio():
    heuristics = ["BF", "BFD", "FF", "FFD", "NF"]

    avg_ratios = []
    for algo in heuristics:
        sub = merged[merged["algo"] == algo]
        avg_ratios.append(sub["avg_ratio"].mean())

    plt.figure(figsize=(8,5))
    plt.bar(heuristics, avg_ratios)
    plt.title("Overall Average Ratio Across All Input Types")
    plt.ylabel("Average Ratio")
    plt.grid(axis='y', alpha=0.3)

    filename = "visualization/figs/group3_summary/overall_avg_ratio.png"
    plt.savefig(filename, dpi=200)
    plt.close()
    print("Saved:", filename)


# =========================
# RUN ALL
# =========================
if __name__ == "__main__":
    plot_ratio_vs_n()
    plot_runtime_vs_n()
    plot_global_avg_ratio()
    print("All graphs generated!")
