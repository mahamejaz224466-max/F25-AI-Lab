import math
def alphabeta(depth, index, max_turn, scores, target, alpha, beta, log):
    if depth == target:
        return scores[index], 1
    leaves = 0
    if max_turn:
        value = float("-inf")
        for i in range(2):
            child, count = alphabeta(depth + 1, index * 2 + i, False, scores, target, alpha, beta, log)
            leaves += count
            value = max(value, child)
            alpha = max(alpha, value)
            if alpha >= beta:
                if i == 0:
                    log.append(f"PRUNE at MAX node depth {depth} index {index}: alpha={alpha} >= beta={beta}")
                break
        return value, leaves
    value = float("inf")
    for i in range(2):
        child, count = alphabeta(depth + 1, index * 2 + i, True, scores, target, alpha, beta, log)
        leaves += count
        value = min(value, child)
        beta = min(beta, value)
        if alpha >= beta:
            if i == 0:
                log.append(f"PRUNE at MIN node depth {depth} index {index}: alpha={alpha} >= beta={beta}")
            break
    return value, leaves


def run(scores):
    depth = int(math.log2(len(scores))) if len(scores) > 1 else 0
    log = []
    value, leaves = alphabeta(0, 0, True, scores, depth, float("-inf"), float("inf"), log)
    return value, leaves, log


if __name__ == "__main__":
    from lab5_minimax import minimax, pad_scores

    trees = [
        ("Tree 1: padded 5.1 scores", pad_scores([3, 5, 2, 9, 0, 7])[0]),
        ("Tree 2: scores from 5.2", [3, 5, 2, 9, 3, 5, 2, 9]),
    ]
    for name, scores in trees:
        depth = int(math.log2(len(scores)))
        mm_value, mm_leaves = minimax(0, 0, True, scores, depth)
        ab_value, ab_leaves, log = run(scores)
        print(name, scores)
        print("Minimax   : value", mm_value, "| leaves evaluated", mm_leaves)
        print("Alpha-beta: value", ab_value, "| leaves evaluated", ab_leaves)
        print("Same value:", mm_value == ab_value)
        print("Pruning events:", log if log else "none")
        print()
