from input_generators import (
    random_uniform,
    random_many_small,
    random_many_large,
    random_bimodal,
    random_perfect_packing,
)
from experiment import run_experiment


if __name__ == "__main__":
    small_ns = [8, 12, 16, 20, 24, 28, 30]
    big_ns = [50, 100, 200]
    L_values = [10, 100]

    small_generators = [
        ("Uniform small n", random_uniform),
        ("Many small items", random_many_small),
        ("Many large items", random_many_large),
        ("Bimodal", random_bimodal),
        ("Perfect packing", random_perfect_packing),
    ]

    big_generators = [
        ("Uniform big n", random_uniform),
        ("Many small items", random_many_small),
        ("Many large items", random_many_large),
        ("Bimodal", random_bimodal),
        ("Perfect packing", random_perfect_packing),
    ]

    # Small n, L = 10
    for L in L_values:
        for n in small_ns:
            for name, gen in small_generators:
                run_experiment(name, gen, n=n, L=10, trials=50)

    # Big n, L = 10 and 100
    for L in L_values:
        for n in big_ns:
            for name, gen in big_generators:
                run_experiment(name, gen, n=n, L=L, trials=50)
