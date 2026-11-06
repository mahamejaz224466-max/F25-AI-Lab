import lab3_bfs_dfs
import lab3_depth_search
import lab3_ucs
from lab3_bfs_dfs import bfs, dfs
from lab3_depth_search import dls, iddfs
from lab3_ucs import ucs

simple = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": ["G"], "F": [], "G": []}
disconnected = {"A": ["B"], "B": [], "H": []}
cycle = {"A": ["B"], "B": ["A", "C"], "C": []}
cycle_weighted = {"A": [("B", 1)], "B": [("A", 1), ("C", 2)], "C": []}

print("Test 1: start equals goal (A to A)")
print("BFS:", bfs(simple, "A", "A")[0])
print("DFS:", dfs(simple, "A", "A")[0])
print("DLS limit 0:", dls(simple, "A", "A", 0))
print("UCS:", ucs({"A": []}, "A", "A")[:2])
print()

print("Test 2: unreachable goal (A to H)")
print("BFS:", bfs(disconnected, "A", "H")[0])
print("DFS:", dfs(disconnected, "A", "H")[0])
print("DLS limit 3:", dls(disconnected, "A", "H", 3))
print("IDDFS max 3:", iddfs(disconnected, "A", "H", 3))
print("UCS:", ucs({"A": [("B", 1)], "B": [], "H": []}, "A", "H")[:2])
print()

print("Test 3: graph with a cycle (A to C)")
print("BFS:", bfs(cycle, "A", "C")[0])
print("DFS:", dfs(cycle, "A", "C")[0])
print("DLS limit 4:", dls(cycle, "A", "C", 4))
print("IDDFS max 4:", iddfs(cycle, "A", "C", 4))
print("UCS:", ucs(cycle_weighted, "A", "C")[:2])
