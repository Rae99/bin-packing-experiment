import random


def random_uniform(n: int, L: int):
    """
    Uniform random items between 1 and L
    """
    return [random.randint(1, L) for _ in range(n)]


def random_many_small(n: int, L: int):
    """
    70% small items (<= L/3), 30% large items (> L/3)
    """
    arr = []
    for _ in range(n):
        if random.random() < 0.7:
            arr.append(random.randint(1, max(1, L // 3)))
        else:
            arr.append(random.randint(max(1, L // 3 + 1), L))
    return arr


def random_many_large(n: int, L: int):
    """
    70% large items (>= L/2), 30% small items (< L/2)
    """
    arr = []
    for _ in range(n):
        if random.random() < 0.7:
            arr.append(random.randint(L // 2, L))
        else:
            arr.append(random.randint(1, max(1, L // 2 - 1)))
    return arr


def random_bimodal(n: int, L: int):
    """
    50% small items (<= L/4), 50% medium items (between L/2 and 3L/4)
    """
    arr = []
    for _ in range(n):
        r = random.random()
        if r < 0.5:
            arr.append(random.randint(1, max(1, L // 4)))
        else:
            arr.append(random.randint(L // 2, min(L, 3 * L // 4)))
    return arr


def random_perfect_packing(num_bins: int, L: int):
    """
    Generate items that perfectly pack into num_bins bins of capacity L.
    """
    sizes = []
    for _ in range(num_bins):
        remaining = L
        while remaining > 0:
            # randint both sides inclusive
            x = random.randint(1, remaining)
            sizes.append(x)
            remaining -= x
    random.shuffle(sizes)
    return sizes
