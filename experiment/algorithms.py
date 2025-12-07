import math
from math import ceil
from ortools.linear_solver import pywraplp


def next_fit(items, L):
    """
    Next-Fit (NF) for 1D bin packing.
    items are used in the given order (no sorting).
    Each item is either put into the current bin or starts a new bin.
    """
    bins_remaining_capacity = []
    placement = []  # placement[i] is the list of items in the i-th bin

    for x in items:
        # if we don't have any bin yet, open the first one
        if not bins_remaining_capacity:
            bins_remaining_capacity.append(L - x)
            placement.append([x])
        else:
            # try to put x into the last bin
            if bins_remaining_capacity[-1] >= x:
                bins_remaining_capacity[-1] -= x
                placement[-1].append(x)
            else:
                # cannot fit into current bin, then open a new one
                bins_remaining_capacity.append(L - x)
                placement.append([x])

    return len(bins_remaining_capacity), placement


def first_fit(items, L):
    """
    First-Fit (FF) for 1D bin packing.
    items are used in the given order (no sorting).
    For each item, scan bins from the first one and put it
    into the first bin that has enough remaining capacity.
    """
    bins_remaining_capacity = []
    placement = []

    for x in items:
        chosen_index = None

        # scan bins from left to right, stop at the first one that fits
        for j, remaining in enumerate(bins_remaining_capacity):
            if remaining >= x:
                chosen_index = j
                break

        if chosen_index is None:
            # open a new bin
            bins_remaining_capacity.append(L - x)
            placement.append([x])
        else:
            bins_remaining_capacity[chosen_index] -= x
            placement[chosen_index].append(x)

    return len(bins_remaining_capacity), placement


def best_fit(items, L):
    """
    Best-Fit (BF) for 1D bin packing.
    items are used in the given order (no sorting).
    For each item, scan all bins and choose the one that would have
    the least remaining capacity after placing this item.
    """
    bins_remaining_capacity = []
    placement = []

    for x in items:
        chosen_index = None
        best_remaining_after = None  # minimal remaining capacity after placing x

        for j, remaining in enumerate(bins_remaining_capacity):
            if remaining >= x:
                after = remaining - x
                if best_remaining_after is None or after < best_remaining_after:
                    best_remaining_after = after
                    chosen_index = j

        if chosen_index is None:
            # open a new bin
            bins_remaining_capacity.append(L - x)
            placement.append([x])
        else:
            bins_remaining_capacity[chosen_index] -= x
            placement[chosen_index].append(x)

    return len(bins_remaining_capacity), placement


def first_fit_decreasing(items, L):
    """
    First-Fit Decreasing (FFD).
    1. sort items in non-increasing order
    2. run First-Fit on this sorted sequence
    """
    items = sorted(items, reverse=True)
    return first_fit(items, L)


def best_fit_decreasing(items, L):
    """
    Best-Fit Decreasing (BFD).
    1. sort items in non-increasing order
    2. run Best-Fit on this sorted sequence
    """
    items = sorted(items, reverse=True)
    return best_fit(items, L)


def exact_bin_packing(items, L):
    """
    Exact solution for 1-D bin Packing using backtracking.
    """

    n = len(items)
    if n == 0:
        return 0, []

    # Sort items in descending order, but keep original indices
    # pairs: [original_index, size]
    # example: if input is [7, 3, 9]
    # paired = [
    #     [0, 7],
    #     [1, 3],
    #     [2, 9],
    # ]
    paired = []
    for i in range(n):
        paired.append([i, items[i]])

    # Sort by size descending
    paired.sort(reverse=True, key=lambda pair: pair[1])
    # example after sort:
    # paired = [
    #     [2, 9],
    #     [0, 7],
    #     [1, 3],
    # ]

    # Extract sorted indices and sizes
    sorted_indices = []
    sorted_items = []
    for pair in paired:
        sorted_indices.append(pair[0])
        sorted_items.append(pair[1])
    # example:
    # sorted_indices = [2, 0, 1]
    # sorted_items = [9, 7, 3]

    # Lower and upper bounds on number of bins
    total = sum(sorted_items)
    lb = math.ceil(total / L)  # minimum possible bins, but may not be feasible
    ub = n  # maximum, each item takes its own bin

    best_k = None
    best_assignment = None

    # starting from the possible lower bound lb, try increasing k and then call search_assignments to find whether a feasible packing which uses k bins exists
    for k in range(lb, ub + 1):

        # Initialize remaining capacity for each bin
        bins_remaining = []
        for _ in range(k):
            bins_remaining.append(L)

        # initialize assignment array, assignment[i] = bin index for each item i, sorted by size descending
        # -1 means at the beginning all items are unassigned
        assignment = []
        for _ in range(n):
            assignment.append(-1)

        # Try to pack all items into k bins
        if search_assignments(0, sorted_items, bins_remaining, assignment):
            best_k = k
            best_assignment = assignment[:]  # make a copy
            break

    # Convert assignment back to original item indices
    bins = []
    for _ in range(best_k):
        bins.append([])

    for sorted_pos in range(n):
        bin_id = best_assignment[sorted_pos]
        orig_idx = sorted_indices[sorted_pos]
        bins[bin_id].append(orig_idx)
    # example:
    # sorted_indices = [2, 0, 1]
    # sorted_items = [9, 7, 3]
    # best_assignment[0] means sorted_items[0] = 9 (original index 2) is placed into bin with bin_idx = best_assignment[0]

    return best_k, bins


def search_assignments(i, items, bins_remaining, assignment):
    """
    Backtracking: try to place item i into one of the bins.

    i: index of current item in 'items'
    items: a list, sizes sorted in descending order
    bins_remaining: a list, remaining capacity in each bin
    assignment: a list, assignment[i] = bin id for item i

    what we are doing: given i, try to assign items[i..end] into bins——bins_remaining shows the number of bins and the remaining capacity of each bin
    return True if a complete feasible assignment is found.
    """

    n = len(items)

    # Base case: all items placed
    if i == n:
        return True

    size_i = items[i]

    # avoid trying bins with the same remaining capacity
    used_capacities = []

    for b in range(len(bins_remaining)):

        cap = bins_remaining[b]

        # Skip if we already tried a bin with the same capacity
        skip = False
        for c in used_capacities:
            if cap == c:
                skip = True
                break
        if skip:
            continue
        used_capacities.append(cap)

        # If item fits into bin b, place it there
        if cap >= size_i:

            bins_remaining[b] -= size_i
            assignment[i] = b

            # Continue with next item
            if search_assignments(i + 1, items, bins_remaining, assignment):
                return True

            # Backtrack
            assignment[i] = -1
            bins_remaining[b] += size_i

    # No bin worked
    return False


def mip_bin_packing(items, L):
    """
    Exact 1-D bin packing using the MIP solver from Google OR-Tools.
    MIP: Mixed Integer Programming model.

    This function is a lightly adapted version of the official OR-Tools
    bin packing example. It's adjusted to fit the experiment.

    The MIP model:
        - Binary variable x[i, j] = 1 if item i is packed in bin j.
        - Binary variable y[j]    = 1 if bin j is used.
        - Each item must be in exactly one bin.
        - The total size in each bin cannot exceed the capacity L.
        - Objective: minimize the number of bins used.
    """

    n = len(items)
    if n == 0:
        return 0, []

    # Create the MIP solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        # Fallback: degenerate solution (each item in its own bin)
        # This should rarely happen, but keeps the interface safe.
        return n, [[i] for i in range(n)]

    # Indices for items and bins.
    # As in the OR-Tools example, we allow at most n bins,
    # one per item in the worst case.
    item_indices = list(range(n))
    bin_indices = list(range(n))

    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    x = {}
    for i in item_indices:
        for j in bin_indices:
            x[(i, j)] = solver.IntVar(0, 1, f"x_{i}_{j}")

    # y[j] = 1 if bin j is used.
    y = {}
    for j in bin_indices:
        y[j] = solver.IntVar(0, 1, f"y_{j}")

    # Constraints
    # Each item must be in exactly one bin.
    for i in item_indices:
        solver.Add(sum(x[(i, j)] for j in bin_indices) == 1)

    # The amount packed in each bin cannot exceed its capacity.
    for j in bin_indices:
        solver.Add(sum(x[(i, j)] * items[i] for i in item_indices) <= y[j] * L)

    # Objective: minimize the number of bins used.
    solver.Minimize(solver.Sum(y[j] for j in bin_indices))

    status = solver.Solve()

    if status != pywraplp.Solver.OPTIMAL:
        # In principle, for small instances we expect an optimal solution.
        # If not, return a simple feasible solution to keep the interface consistent.
        return n, [[i] for i in range(n)]

    # Extract the solution: placement[b] is a list of original item indices in bin b.
    placement = []
    for j in bin_indices:
        if y[j].solution_value() > 0.5:  # bin j is used
            bin_items = []
            for i in item_indices:
                if x[(i, j)].solution_value() > 0.5:
                    bin_items.append(i)
            if bin_items:
                placement.append(bin_items)

    num_bins = len(placement)
    return num_bins, placement
