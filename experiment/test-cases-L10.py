from experiment.algorithms import (
    next_fit,
    first_fit,
    best_fit,
    first_fit_decreasing,
    best_fit_decreasing,
    exact_bin_packing,
)

if __name__ == "__main__":
    print("Strip Packing Algorithms Test Cases")
    print("--------------------------------")
    # Example
    print("Example:")
    L = 10
    lengths = [7, 6, 4, 4, 3, 3, 2, 2]
    print("Strip length L =", L)
    print("Items:", lengths)
    for name, func in [
        ("NF", next_fit),
        ("FF", first_fit),
        ("BF", best_fit),
        ("FFD", first_fit_decreasing),
        ("BFD", best_fit_decreasing),
        ("Exact", exact_bin_packing),
    ]:
        strips_used, placement = func(lengths, L)
        print(f"{name}: strips used = {strips_used}, placement = {placement}")
    print("--------------------------------")

    # Counterexample
    print("Counterexample:")
    L = 10
    lengths = [6, 5, 3, 2, 2, 2]
    print("Strip length L =", L)
    print("Items:", lengths)
    for name, func in [
        ("NF", next_fit),
        ("FF", first_fit),
        ("BF", best_fit),
        ("FFD", first_fit_decreasing),
        ("BFD", best_fit_decreasing),
        ("Exact", exact_bin_packing),
    ]:
        strips_used, placement = func(lengths, L)
        print(f"{name}: strips used = {strips_used}, placement = {placement}")

    # test cases
    print("Test cases:")
    print("--------------------------------")
    lengths = [5, 2, 2, 3, 4, 4, 9, 1]
    print(lengths)
    for name, func in [
        ("NF", next_fit),
        ("FF", first_fit),
        ("BF", best_fit),
        ("FFD", first_fit_decreasing),
        ("BFD", best_fit_decreasing),
        ("Exact", exact_bin_packing),
    ]:
        strips_used, placement = func(lengths, L)
        print(f"{name}: strips used = {strips_used}, placement = {placement}")

    print("--------------------------------")
    # test cases
    lengths = [2, 2, 2, 2, 2]
    print(lengths)
    print(lengths)
    for name, func in [
        ("NF", next_fit),
        ("FF", first_fit),
        ("BF", best_fit),
        ("FFD", first_fit_decreasing),
        ("BFD", best_fit_decreasing),
        ("Exact", exact_bin_packing),
    ]:
        strips_used, placement = func(lengths, L)
        print(f"{name}: strips used = {strips_used}, placement = {placement}")

    L = 10
    lengths = [2, 2, 2, 2, 2, 2]
    print(lengths)
    for name, func in [
        ("NF", next_fit),
        ("FF", first_fit),
        ("BF", best_fit),
        ("FFD", first_fit_decreasing),
        ("BFD", best_fit_decreasing),
        ("Exact", exact_bin_packing),
    ]:
        strips_used, placement = func(lengths, L)
        print(f"{name}: strips used = {strips_used}, placement = {placement}")

    L = 10
    lengths = [7, 7, 3, 3, 3]
    print(lengths)
    for name, func in [
        ("NF", next_fit),
        ("FF", first_fit),
        ("BF", best_fit),
        ("FFD", first_fit_decreasing),
        ("BFD", best_fit_decreasing),
        ("Exact", exact_bin_packing),
    ]:
        strips_used, placement = func(lengths, L)
        print(f"{name}: strips used = {strips_used}, placement = {placement}")

    L = 10
    lengths = [4, 4, 4, 6, 6, 6]
    print(lengths)
    for name, func in [
        ("NF", next_fit),
        ("FF", first_fit),
        ("BF", best_fit),
        ("FFD", first_fit_decreasing),
        ("BFD", best_fit_decreasing),
        ("Exact", exact_bin_packing),
    ]:
        strips_used, placement = func(lengths, L)
        print(f"{name}: strips used = {strips_used}, placement = {placement}")

    L = 10
    lengths = [2, 2, 2, 3, 5, 6]
    print(lengths)
    for name, func in [
        ("NF", next_fit),
        ("FF", first_fit),
        ("BF", best_fit),
        ("FFD", first_fit_decreasing),
        ("BFD", best_fit_decreasing),
        ("Exact", exact_bin_packing),
    ]:
        strips_used, placement = func(lengths, L)
        print(f"{name}: strips used = {strips_used}, placement = {placement}")

    L = 10
    lengths = [4, 3, 3, 3, 3, 2, 2, 2]
    print(lengths)
    for name, func in [
        ("NF", next_fit),
        ("FF", first_fit),
        ("BF", best_fit),
        ("FFD", first_fit_decreasing),
        ("BFD", best_fit_decreasing),
        ("Exact", exact_bin_packing),
    ]:
        strips_used, placement = func(lengths, L)
        print(f"{name}: strips used = {strips_used}, placement = {placement}")

    L = 10
    lengths = [9, 8, 7, 6, 5, 5, 2, 2, 1]
    print(lengths)
    for name, func in [
        ("NF", next_fit),
        ("FF", first_fit),
        ("BF", best_fit),
        ("FFD", first_fit_decreasing),
        ("BFD", best_fit_decreasing),
        ("Exact", exact_bin_packing),
    ]:
        strips_used, placement = func(lengths, L)
        print(f"{name}: strips used = {strips_used}, placement = {placement}")
