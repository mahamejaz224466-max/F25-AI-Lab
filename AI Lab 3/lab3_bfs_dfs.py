from collections import deque

graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": ["G"], "F": [], "G": []}


def bfs(graph, start, goal):
    q = deque([(start, [start])])
    seen = {start}
    order = []
    steps = []
    while q:
        node, path = q.popleft()
        order.append(node)
        if node == goal:
            steps.append((node, path, [n for n, p in q]))
            return path, order, steps
        for n in graph[node]:
            if n not in seen:
                seen.add(n)
                q.append((n, path + [n]))
        steps.append((node, path, [n for n, p in q]))
    return None, order, steps


def dfs(graph, start, goal):
    stack = [(start, [start])]
    seen = set()
    order = []
    steps = []
    while stack:
        node, path = stack.pop()
        if node == goal:
            order.append(node)
            steps.append((node, path, [n for n, p in stack]))
            return path, order, steps
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        for n in reversed(graph[node]):
            stack.append((n, path + [n]))
        steps.append((node, path, [n for n, p in stack]))
    return None, order, steps


def show(name, result):
    path, order, steps = result
    print(name)
    print("step    processed    path    frontier after")
    for i, (node, p, frontier) in enumerate(steps, 1):
        print(i,  node, "->".join(p),frontier)
    print("Final path:", path)
    print("Visit order:", order)
    print()


if __name__ == "__main__":
    show("BFS", bfs(graph, "A", "G"))
    show("DFS (stack top is the right end)", dfs(graph, "A", "G"))
