from collections import Counter
from itertools import combinations


def main():
    pair_counts = Counter();
    pairs = combinations(sorted([1, 2, 3,2]), 2)
    print(pairs)
    pair_counts.update(pairs)
    print(pair_counts)


if __name__ == "__main__":
    main()
