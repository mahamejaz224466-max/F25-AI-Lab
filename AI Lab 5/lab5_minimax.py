import math
def minimax(depth, index, max_turn, scores, target):
    if depth == target:
        return scores[index], 1
    left, left_count = minimax(depth + 1, index * 2, not max_turn, scores, target)
    right, right_count = minimax(depth + 1, index * 2 + 1, not max_turn, scores, target)
    if max_turn:
        return max(left, right), left_count + right_count
    return min(left, right), left_count + right_count


def pad_scores(scores):
    tree_depth = math.ceil(math.log2(len(scores))) if len(scores) > 1 else 0
    return scores + [0] * (2 ** tree_depth - len(scores)), tree_depth


def trace(scores, target):
    print("Level by level values (leaves -> root)")
    values = list(scores)
    max_turn_levels = []
    for level in range(target - 1, -1, -1):
        is_max = level % 2 == 0
        new_values = []
        for i in range(0, len(values), 2):
            if is_max:
                new_values.append(max(values[i], values[i + 1]))
            else:
                new_values.append(min(values[i], values[i + 1]))
        print("depth", level, "(MAX)" if is_max else "(MIN)", values, "->", new_values)
        values = new_values
    return values[0]


if __name__ == "__main__":
    original = [3, 5, 2, 9, 0, 7]
    scores, depth = pad_scores(list(original))
    print("Supplied scores:", original)
    print("Padded scores:", scores)
    print("Tree depth:", depth)
    print()
    root = trace(scores, depth)
    print()
    value, leaves = minimax(0, 0, True, scores, depth)
    print("Minimax value:", value)
    print("Leaves evaluated:", leaves)
    print("Hand trace root value:", root)
