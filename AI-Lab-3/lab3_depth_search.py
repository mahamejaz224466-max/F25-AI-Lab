# Lab 3 - Task 2: depth-limited search (DLS) and iterative deepening (IDDFS).
# Root has depth 0. Cycle check is PATH-LOCAL (a node already on the current path
# is skipped); there is no global visited set, so valid revisits are not suppressed.
# Statuses: FOUND, CUTOFF (a deeper unexplored continuation exists), FAILURE
# (the explored branch is exhausted, nothing was cut off).
# Counts: 'nodes processed' = nodes entered by DLS, goal included.
from lab3_bfs_dfs import graph

FOUND, CUTOFF, FAILURE = "FOUND", "CUTOFF", "FAILURE"

def dls(start, goal, limit, graph=graph):
    counter = {"n": 0}
    def rec(node, path, depth):
        counter["n"] += 1
        if node == goal:
            return FOUND, path
        if depth == limit:
            has_more = any(n not in path for n in graph[node])
            return (CUTOFF, None) if has_more else (FAILURE, None)
        cutoff = False
        for n in graph[node]:
            if n in path:          # path-local cycle check
                continue
            status, res = rec(n, path + [n], depth + 1)
            if status == FOUND: return FOUND, res
            if status == CUTOFF: cutoff = True
        return (CUTOFF, None) if cutoff else (FAILURE, None)
    status, path = rec(start, [start], 0)
    return status, path, counter["n"]

def iddfs(start, goal, max_depth, graph=graph):
    attempted, total = [], 0
    status, path = FAILURE, None
    for limit in range(0, max_depth + 1):
        attempted.append(limit)
        status, path, n = dls(start, goal, limit, graph)
        total += n
        if status != CUTOFF:       # FOUND, or FAILURE (nothing deeper to try)
            break
    return status, path, attempted, total

if __name__ == "__main__":
    print("== DLS (A -> G), limits 1-4 ==")
    print("limit | status | path | nodes processed")
    for L in (1, 2, 3, 4):
        s, p, n = dls("A", "G", L)
        print(L, s, "->".join(p) if p else None, n, sep=" | ")
    print("\n== IDDFS (A -> G), max depth 1-4 ==")
    print("max depth | status | path | limits attempted | total nodes processed")
    for M in (1, 2, 3, 4):
        s, p, att, tot = iddfs("A", "G", M)
        print(M, s, "->".join(p) if p else None, att, tot, sep=" | ")
    print("\nPer-iteration cost of IDDFS limits 0-3 (shows repeated work):")
    for L in range(0, 4):
        s, p, n = dls("A", "G", L)
        print(f"  limit {L}: {s}, {n} nodes processed")
