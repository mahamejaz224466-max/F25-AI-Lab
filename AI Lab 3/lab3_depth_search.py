graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": ["G"], "F": [], "G": []}


def dls(graph, node, goal, limit, path=None):
    if path is None:
        path = [node]
    if node == goal:
        return "FOUND", path
    if limit == 0:
        for n in graph.get(node, []):
            if n not in path:
                return "CUTOFF", None
        return "FAILURE", None
    cutoff = False
    for n in graph.get(node, []):
        if n in path:
            continue
        status, result = dls(graph, n, goal, limit - 1, path + [n])
        if status == "FOUND":
            return status, result
        if status == "CUTOFF":
            cutoff = True
    if cutoff:
        return "CUTOFF", None
    return "FAILURE", None


def iddfs(graph, start, goal, max_depth):
    attempted = []
    for limit in range(max_depth + 1):
        status, path = dls(graph, start, goal, limit)
        attempted.append(limit)
        if status == "FOUND":
            return "FOUND", path, attempted
        if status == "FAILURE":
            return "FAILURE", None, attempted
    return "CUTOFF", None, attempted


if __name__ == "__main__":
    print("DLS from A to G")
    for limit in [1, 2, 3, 4]:
        status, path = dls(graph, "A", "G", limit)
        print("limit", limit , status, path)
    print()
    print("IDDFS from A to G")
    for max_depth in [1, 2, 3, 4]:
        status, path, attempted = iddfs(graph, "A", "G", max_depth)
        print("max depth", max_depth, status, path, " limits attempted", attempted)
