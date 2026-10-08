# Lab 3 - Section 3.2 / Task 1: BFS and DFS on the original A-G graph.
# bfs() and dfs() are the manual's supplied code (unchanged logic). The *_trace()
# versions mirror them and record each step so the manual trace can be verified.
# Trace convention: a node is listed when it is REMOVED from the queue/stack and
# processed (goal included); already-processed duplicates are skipped.
from collections import deque

graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": ["G"], "F": [], "G": []}

def bfs(start, goal, graph=graph):
    q = deque([(start, [start])]); seen = {start}
    while q:
        node, path = q.popleft()
        if node == goal: return path
        for n in graph[node]:
            if n not in seen:
                seen.add(n); q.append((n, path + [n]))

def dfs(start, goal, graph=graph):
    stack = [(start, [start])]; seen = set()
    while stack:
        node, path = stack.pop()
        if node == goal: return path
        if node in seen: continue
        seen.add(node)
        for n in reversed(graph[node]): stack.append((n, path + [n]))

def bfs_trace(start, goal, graph=graph):
    q = deque([(start, [start])]); seen = {start}; steps = []
    while q:
        node, path = q.popleft()
        if node == goal:
            steps.append((node, path, [p[0] for p in q])); return path, steps
        for n in graph[node]:
            if n not in seen:
                seen.add(n); q.append((n, path + [n]))
        steps.append((node, path, [p[0] for p in q]))
    return None, steps

def dfs_trace(start, goal, graph=graph):
    stack = [(start, [start])]; seen = set(); steps = []
    while stack:
        node, path = stack.pop()
        if node == goal:
            steps.append((node, path, [p[0] for p in stack])); return path, steps
        if node in seen: continue
        seen.add(node)
        for n in reversed(graph[node]): stack.append((n, path + [n]))
        steps.append((node, path, [p[0] for p in stack]))
    return None, steps

def show(name, trace_fn, plain_fn, frontier_label):
    path, steps = trace_fn("A", "G")
    print(f"== {name} ==")
    print(f"step | processed | path so far | {frontier_label} after step")
    for i, (node, p, fr) in enumerate(steps, 1):
        print(i, node, "->".join(p), fr, sep=" | ")
    print("visit order :", [s[0] for s in steps])
    print("final path  :", path)
    assert path == plain_fn("A", "G"), "trace disagrees with supplied code!"
    print("verified against supplied code: OK\n")

if __name__ == "__main__":
    show("BFS", bfs_trace, bfs, "queue (front first)")
    show("DFS", dfs_trace, dfs, "stack (top is rightmost)")
