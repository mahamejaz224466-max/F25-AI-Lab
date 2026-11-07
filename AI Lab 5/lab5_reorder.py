import math
import random
from lab5_minimax import minimax, pad_scores
from lab5_alphabeta import run

def build(leaves):
    if len(leaves) == 1:
        return leaves[0]
    half = len(leaves) // 2
    return [build(leaves[:half]), build(leaves[half:])]


def flatten(tree):
    if not isinstance(tree, list):
        return [tree]
    return flatten(tree[0]) + flatten(tree[1])


def orderings(tree):
    if not isinstance(tree, list):
        return [tree]
    result = []
    for left in orderings(tree[0]):
        for right in orderings(tree[1]):
            result.append([left, right])
            result.append([right, left])
    return result


if __name__ == "__main__":
    base = pad_scores([3, 5, 2, 9, 0, 7])[0]
    depth = int(math.log2(len(base)))
    mm_value, mm_leaves = minimax(0, 0, True, base, depth)
    print("Original order:", base)
    print("Minimax value:", mm_value, "| leaves:", mm_leaves)
    print()

    results = []
    seen = set()
    for tree in orderings(build(base)):
        leaves = tuple(flatten(tree))
        if leaves in seen:
            continue
        seen.add(leaves)
        value, count, log = run(list(leaves))
        results.append((count, list(leaves), value))
    results.sort(key=lambda r: r[0])

    print("Distinct child-swap orderings tried:", len(results))
    print("All alpha-beta values equal minimax value:", all(r[2] == mm_value for r in results))
    print("Fewest leaves:", results[0][0], "with order", results[0][1])
    print("Most leaves  :", results[-1][0], "with order", results[-1][1])
    counts = {}
    for r in results:
        counts[r[0]] = counts.get(r[0], 0) + 1
    print("Leaves evaluated -> number of orderings:", dict(sorted(counts.items())))
    print()

    print("Selected orderings")
    selected = [
        ("original", [3, 5, 2, 9, 0, 7, 0, 0]),
        ("best found", results[0][1]),
        ("worst found", results[-1][1]),
    ]
    for name, order in selected:
        value, count, log = run(order)
        print(name, order, "| value", value, "| leaves", count)
        for entry in log:
            print("   ", entry)
    print()

    print("Edge case tests")
    print("Single leaf [4]:", minimax(0, 0, True, [4], 0), run([4])[:2])
    print("All equal [7]*8:", minimax(0, 0, True, [7] * 8, 3), run([7] * 8)[:2])
    random.seed(1)
    ok = True
    never_more = True
    saved = 0
    for _ in range(1000):
        scores = [random.randint(-10, 10) for _ in range(16)]
        mm_v, mm_c = minimax(0, 0, True, scores, 4)
        ab_v, ab_c, log = run(scores)
        if mm_v != ab_v:
            ok = False
        if ab_c > mm_c:
            never_more = False
        saved += mm_c - ab_c
    print("1000 random 16-leaf trees: same value:", ok, "| alpha-beta never more leaves:", never_more)
    print("Average leaves saved per tree:", saved / 1000)
