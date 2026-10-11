# Lab 4 - Informed search: A* on the S-A-B-C-G campus graph, heuristic audit,
# A* vs UCS comparison and the single-value overestimate experiment.

# astar() is the manual's supplied code (unchanged). astar_trace() mirrors it and
# records every queue pop so counts come from the trace, not from guessing.
# Conventions (fixed for ALL runs):
#   * Queue entries are (f, g, node, path); ties break by smaller g, then by node name.
#   * 'Expanded' = a non-stale node whose successors are examined. The goal is
#     processed (logged) but NOT counted as an expansion.
#   * Stale entries (g != best[node]) are skipped and counted separately.
# Edge weights are abstract travel-time units; h values are abstract time estimates.

import heapq

def astar(graph, h, start, goal):
    pq = [(h[start], 0, start, [start])]; best = {start: 0}
    while pq:
        f, g, node, path = heapq.heappop(pq)
        if node == goal: return g, path
        if g != best[node]: continue
        for nxt, w in graph.get(node, []):
            ng = g + w
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                heapq.heappush(pq, (ng + h[nxt], ng, nxt, path + [nxt]))

def astar_trace(graph, h, start, goal):

    # Same algorithm as astar(); returns (cost, path, log, expanded, stale).

    pq = [(h[start], 0, start, [start])]; best = {start: 0}
    log, expanded, stale = [], 0, 0
    while pq:
        f, g, node, path = heapq.heappop(pq)
        entry = {"node": node, "g": g, "h": h[node], "f": f, "status": ""}
        if node == goal:
            entry["status"] = "GOAL (processed, not counted as expansion)"
            entry["frontier"] = sorted(pq)
            log.append(entry)
            return g, path, log, expanded, stale
        if g != best[node]:
            stale += 1; entry["status"] = "STALE (skipped)"
            entry["frontier"] = sorted(pq); log.append(entry); continue
        expanded += 1; entry["status"] = "expanded"
        for nxt, w in graph.get(node, []):
            ng = g + w
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                heapq.heappush(pq, (ng + h[nxt], ng, nxt, path + [nxt]))
        entry["frontier"] = sorted(pq)
        log.append(entry)
    return None, None, log, expanded, stale

def path_cost(graph, path):

    # Independent re-sum of edge weights along a path.

    total = 0
    for u, v in zip(path, path[1:]):
        total += dict(graph[u])[v]
    return total

def true_remaining(graph, goal):

    # Exact cheapest cost from every node to goal (Bellman-Ford style relaxation).

    dist = {n: float("inf") for n in graph}; dist[goal] = 0
    for _ in range(len(graph)):
        for u, edges in graph.items():
            for v, w in edges:
                if dist[v] + w < dist[u]: dist[u] = dist[v] + w
    return dist

def audit(graph, h, goal):
    true = true_remaining(graph, goal)
    print("  admissibility  h(n) <= true remaining cost:")
    adm = True
    for n in graph:
        ok = h[n] <= true[n]; adm &= ok
        print(f"    {n}: h={h[n]}  true={true[n]}  {'OK' if ok else 'VIOLATED'}")
    print("  consistency  h(u) <= cost(u,v) + h(v) for each edge:")
    con = True
    for u, edges in graph.items():
        for v, w in edges:
            ok = h[u] <= w + h[v]; con &= ok
            print(f"    {u}->{v}: {h[u]} <= {w} + {h[v]} = {w + h[v]}  {'OK' if ok else 'VIOLATED'}")
    print(f"  => admissible: {adm} | consistent: {con}")
    return adm, con

def run(name, graph, h, start, goal):
    cost, path, log, exp, stale = astar_trace(graph, h, start, goal)
    assert (cost, path) == astar(graph, h, start, goal), "trace disagrees with supplied astar!"
    print(f"{name}")
    print("step | node | g | h | f | status | frontier after (f,g,node)")
    for i, e in enumerate(log, 1):
        fr = [(f, g, n) for f, g, n, _ in e["frontier"]]
        print(i, e["node"], e["g"], e["h"], e["f"], e["status"], fr, sep=" | ")
    print("returned path     :", "->".join(path), "| returned cost:", cost)
    print("independent sum   :", path_cost(graph, path))
    print("processed order   :", [e["node"] for e in log])
    print(f"expanded count    : {exp} | stale skipped: {stale} | goal processed: 1")
    return cost, path, exp

graph = {"S": [("A", 1), ("B", 4)], "A": [("C", 2)], "B": [("G", 5)], "C": [("G", 3)], "G": []}
H = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}

if __name__ == "__main__":
    print("Supplied astar() on the campus graph:", astar(graph, H, "S", "G"))
    print("Heuristic audit (supplied h)")
    audit(graph, H, "G")
    r1 = run("TASK 2: A* with supplied heuristic", graph, H, "S", "G")
    H0 = {n: 0 for n in H}
    r2 = run("TASK 2 control: UCS (all h = 0)", graph, H0, "S", "G")
    Hc = dict(H); Hc["C"] = 10
    print("Task 3: overestimate h(C) 2 -> 10 (true remaining cost of C = 3)")
    audit(graph, Hc, "G")
    r3 = run("TASK 3: A* with h(C)=10", graph, Hc, "S", "G")
    print("Summary table")
    print("run | path | cost | expanded")
    for name, r in (("A* (supplied h)", r1), ("UCS (h=0)", r2), ("A* with h(C)=10", r3)):
        print(name, "->".join(r[1]), r[0], r[2], sep=" | ")
