import heapq

weighted_graph = {
    "A": [("B", 1), ("C", 2)],
    "B": [("D", 4), ("E", 1)],
    "C": [("F", 5), ("G", 10)],
    "D": [],
    "E": [("G", 1)],
    "F": [],
    "G": [],
}


def ucs(graph, start, goal):
    counter = 0
    frontier = [(0, counter, start, [start])]
    explored = set()
    order = []
    while frontier:
        cost, _, node, path = heapq.heappop(frontier)
        if node in explored:
            continue
        explored.add(node)
        order.append((node, cost))
        if node == goal:
            return path, cost, order
        for neighbor, weight in graph[node]:
            if neighbor not in explored:
                counter += 1
                heapq.heappush(frontier, (cost + weight, counter, neighbor, path + [neighbor]))
    return None, None, order


def bfs_weighted(graph, start, goal):
    from collections import deque
    q = deque([(start, [start])])
    seen = {start}
    order = []
    while q:
        node, path = q.popleft()
        order.append(node)
        if node == goal:
            return path, order
        for neighbor, weight in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                q.append((neighbor, path + [neighbor]))
    return None, order


def path_cost(graph, path):
    total = 0
    for a, b in zip(path, path[1:]):
        for neighbor, weight in graph[a]:
            if neighbor == b:
                total += weight
    return total


if __name__ == "__main__":
    print("Weighted graph (directed edges)")
    for node, edges in weighted_graph.items():
        for neighbor, weight in edges:
            print(node, "->", neighbor, "cost", weight)
    print()
    path, cost, order = ucs(weighted_graph, "A", "G")
    print("UCS path:", path)
    print("UCS reported cost:", cost)
    print("UCS independent cost check:", path_cost(weighted_graph, path))
    print("UCS processing order (node, cost so far):", order)
    print("UCS hops:", len(path) - 1)
    print()
    bpath, border = bfs_weighted(weighted_graph, "A", "G")
    print("BFS path:", bpath)
    print("BFS cost:", path_cost(weighted_graph, bpath))
    print("BFS processing order:", border)
    print("BFS hops:", len(bpath) - 1)
