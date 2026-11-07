import heapq

graph = {"S": [("A", 1), ("B", 4)], "A": [("C", 2)], "B": [("G", 5)], "C": [("G", 3)], "G": []}
h = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}


def astar(graph, h, start, goal):
    pq = [(h[start], 0, start, [start])]
    best = {start: 0}
    processed = []
    expanded = []
    stale = 0
    snapshots = []
    while pq:
        f, g, node, path = heapq.heappop(pq)
        if g != best[node]:
            stale += 1
            continue
        processed.append((node, g, h[node], f))
        if node == goal:
            return {"cost": g, "path": path, "processed": processed, "expanded": expanded, "stale": stale, "snapshots": snapshots}
        expanded.append(node)
        for nxt, w in graph.get(node, []):
            ng = g + w
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                heapq.heappush(pq, (ng + h[nxt], ng, nxt, path + [nxt]))
        snapshots.append((node, sorted([(item[0], item[1], item[2]) for item in pq])))
    return {"cost": None, "path": None, "processed": processed, "expanded": expanded, "stale": stale, "snapshots": snapshots}


def path_cost(graph, path):
    total = 0
    for a, b in zip(path, path[1:]):
        for nxt, w in graph[a]:
            if nxt == b:
                total += w
    return total


def true_remaining(graph, goal):
    costs = {}
    for node in graph:
        zero = {n: 0 for n in graph}
        result = astar(graph, zero, node, goal)
        costs[node] = result["cost"]
    return costs


def report(name, result, graph):
    print(name)
    print("Path:", result["path"])
    print("Returned cost:", result["cost"])
    print("Independent cost check:", path_cost(graph, result["path"]))
    print("Processed nodes (node, g, h, f):")
    for item in result["processed"]:
        print("  ", item)
    print("Expanded nodes:", result["expanded"])
    print("Expansion count:", len(result["expanded"]))
    print("Stale entries skipped:", result["stale"])
    print()


if __name__ == "__main__":
    print("Heuristic audit")
    true_costs = true_remaining(graph, "G")
    for node in graph:
        status = "OK" if h[node] <= true_costs[node] else "OVERESTIMATE"
        print(node, "h =", h[node], "true remaining =", true_costs[node], status)
    print()
    for u in graph:
        for v, w in graph[u]:
            status = "OK" if h[u] <= w + h[v] else "FAIL"
            print(f"edge {u}->{v}: h({u}) = {h[u]} <= {w} + h({v}) = {w + h[v]} {status}")
    print()

    a_result = astar(graph, h, "S", "G")
    report("A* with supplied heuristic", a_result, graph)
    print("Frontier after each expansion (f, g, node)")
    for node, frontier in a_result["snapshots"]:
        print("after expanding", node, ":", frontier)
    print()

    zero = {n: 0 for n in graph}
    u_result = astar(graph, zero, "S", "G")
    report("UCS control (all h = 0)", u_result, graph)

    print("Comparison")
    print("A* expansions:", len(a_result["expanded"]), "| UCS expansions:", len(u_result["expanded"]))
    print()

    h_bad = dict(h)
    h_bad["C"] = 10
    print("Overestimate experiment: h(C) changed from", h["C"], "to", h_bad["C"], "| true remaining cost of C =", true_costs["C"])
    b_result = astar(graph, h_bad, "S", "G")
    report("A* with h(C) = 10", b_result, graph)
    print("Original A*: cost", a_result["cost"], "path", a_result["path"], "expansions", len(a_result["expanded"]))
    print("Modified A*: cost", b_result["cost"], "path", b_result["path"], "expansions", len(b_result["expanded"]))
    print()

    print("Edge case tests")
    same = astar(graph, h, "S", "S")
    print("Start equals goal:", same["path"], same["cost"])
    cut = {"S": [("A", 1)], "A": [], "G": []}
    lost = astar(cut, {"S": 0, "A": 0, "G": 0}, "S", "G")
    print("Unreachable goal:", lost["path"], lost["cost"])
