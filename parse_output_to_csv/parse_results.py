import csv

INPUT_PATH = "experiment_direct_output/output3.txt"
ALGO_CSV = "parse_output_to_csv/algo_results_manual.csv"
SOLVER_CSV = "parse_output_to_csv/solver_results_manual.csv"


def parse_experiments(path):
    with open(path, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    algo_rows = []
    solver_rows = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Detect the beginning of an experiment block
        if line.startswith("=== Experiment:"):
            # Example:
            # === Experiment: Uniform small n, n=8, L=10, trials=50 ===
            inner = line.split("Experiment:")[1].strip(" =")
            parts = [p.strip() for p in inner.split(",")]

            dist = parts[0]  # e.g., "Uniform small n"
            n = int(parts[1].split("=")[1])  # n=8
            L = int(parts[2].split("=")[1])  # L=10
            trials = int(parts[3].split("=")[1])  # trials=50

            # Next line should be the "Algo ..." header
            i += 1  # Move to "Algo ..." line
            if i < len(lines) and lines[i].startswith("Algo"):
                i += 1  # Move to first heuristic result row
            else:
                # Should not happen, but skip defensively
                i += 1

            # Parse heuristic results table
            while i < len(lines):
                l = lines[i].strip()

                # Blank line → end of heuristic table
                if not l:
                    i += 1
                    break

                # Some experiments may skip exact solvers.
                # If we hit a new experiment or "Exact solvers", stop.
                if l.startswith("===") or l.startswith("Exact solvers"):
                    break

                # Example:
                # NF  5.74000000   0.002   1.13500000
                # or:
                # NF  35.22000000  0.006   -
                parts = l.split()
                algo = parts[0]
                avg_bins = float(parts[1])
                avg_time_ms = float(parts[2])

                # Ratio might be a number or "-"
                ratio_str = parts[3] if len(parts) > 3 else "-"
                avg_ratio = None if ratio_str == "-" else float(ratio_str)

                algo_rows.append(
                    {
                        "dist": dist,
                        "n": n,
                        "L": L,
                        "trials": trials,
                        "algo": algo,
                        "avg_bins": avg_bins,
                        "avg_time_ms": avg_time_ms,
                        "avg_ratio": avg_ratio,
                    }
                )
                i += 1

            # Check if an "Exact solvers" section follows
            if i < len(lines) and lines[i].startswith("Exact solvers"):
                i += 1  # Move to "Solver ..." header
                if i < len(lines) and lines[i].startswith("Solver"):
                    i += 1  # Move to first solver result row

                # Parse solver results
                while i < len(lines):
                    l = lines[i].strip()

                    # Blank line → end of solver table
                    if not l:
                        i += 1
                        break

                    # Stop when hitting "Estimated OPT" or next experiment
                    if l.startswith("Estimated OPT") or l.startswith("==="):
                        break

                    # Example:
                    # my_own_exact_solver  5.12000000   0.016
                    parts = l.split()
                    solver_name = parts[0]
                    avg_bins = float(parts[1])
                    avg_time_ms = float(parts[2])

                    solver_rows.append(
                        {
                            "dist": dist,
                            "n": n,
                            "L": L,
                            "trials": trials,
                            "solver": solver_name,
                            "avg_bins": avg_bins,
                            "avg_time_ms": avg_time_ms,
                        }
                    )
                    i += 1

            # If no "Exact solvers" exists, simply continue scanning
        else:
            i += 1

    return algo_rows, solver_rows


def write_csv(rows, path, fieldnames):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    algo_rows, solver_rows = parse_experiments(INPUT_PATH)

    write_csv(
        algo_rows,
        ALGO_CSV,
        ["dist", "n", "L", "trials", "algo", "avg_bins", "avg_time_ms", "avg_ratio"],
    )

    write_csv(
        solver_rows,
        SOLVER_CSV,
        ["dist", "n", "L", "trials", "solver", "avg_bins", "avg_time_ms"],
    )

    print(f"Wrote {len(algo_rows)} algo rows to {ALGO_CSV}")
    print(f"Wrote {len(solver_rows)} solver rows to {SOLVER_CSV}")


if __name__ == "__main__":
    main()
