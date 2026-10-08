# Lab 3 - Task 3: weighted graph, UCS, and BFS comparison on the same topology.
# Section 3.7 extension: original vertices/corridors plus the added corridor C->G.
# The manual's weight table was not in the text I had, so these weights are my own
# choice, picked to match the manual's stated results (BFS A-C-G cost 12; UCS
# A-B-E-G cost 3). All weights are nonnegative travel-cost units (synthetic).
# Tie-break: equal path cost -> the entry inserted earlier is processed first.
import heapq
from lab3_bfs_dfs import bfs

# Directed corridors, successor order = tie-breaking order.
wgraph = {
    "A": [("B", 1), ("C", 5)],
    "B": [("D", 2), ("E", 1)],
    "C": [("F", 2), ("G", 7)],     # C->G is the ADDED corridor
    "D": [],
    "E": [("G", 1)],
    "F": [],
    "G": [],
}
unweighted = {k: [n for n, _ in v] for k, v in wgraph.items()}

def ucs(start, goal, wg=wgraph):
    for u, edges in wg.items():
        for v, w in edges:
            if w < 0: raise ValueError(f"negative weight on {u}->{v}; UCS needs w >= 0")
    counter = 0
    pq = [(0, counter, start, [start])]
    explored, order = set(), []
    while pq:
        cost, _, node, path = heapq.heappop(pq)
        if node in explored: continue
        explored.add(node); order.append((node, cost))
        if node == goal:
            return path, cost, order
        for n, w in wg[node]:
            if n not in explored:
                counter += 1
                heapq.heappush(pq, (cost + w, counter, n, path + [n]))
    return None, None, order

def path_cost(path, wg=wgraph):
    """Independent re-sum of edge weights (does not reuse UCS's running cost)."""
    total = 0
    for u, v in zip(path, path[1:]):
        total += dict(wg[u])[v]
    return total

if __name__ == "__main__":
    print("Weighted edges (directed):")
    for u, edges in wgraph.items():
        for v, w in edges:
            print(f"  {u}->{v} = {w}" + ("   (added corridor)" if (u, v) == ("C", "G") else ""))
    p, c, order = ucs("A", "G")
    print("\nUCS path          :", "->".join(p), "| reported cost:", c, "| hops:", len(p) - 1)
    print("UCS processing    :", " , ".join(f"{n}({k})" for n, k in order))
    print("independent sum   :", path_cost(p))
    assert path_cost(p) == c
    bp = bfs("A", "G", unweighted)
    print("\nBFS path          :", "->".join(bp), "| hops:", len(bp) - 1, "| total cost:", path_cost(bp))
    print("\nComparison: UCS cost", c, "vs BFS cost", path_cost(bp),
          "| UCS hops", len(p) - 1, "vs BFS hops", len(bp) - 1)
