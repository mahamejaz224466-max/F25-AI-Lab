# Lab 3 - Section 3.8 edge cases: start == goal, unreachable goal, cycle graph.
from lab3_bfs_dfs import bfs, dfs, graph
from lab3_depth_search import dls, iddfs
from lab3_ucs import ucs, wgraph

cyc = {"A": ["B"], "B": ["C"], "C": ["A", "D"], "D": [], "Z": []}   # A-B-C-A cycle; Z isolated

print("1) start == goal (A -> A)")
print("  BFS", bfs("A", "A"), "| DFS", dfs("A", "A"), "| DLS(0)", dls("A", "A", 0)[:2],
      "| UCS", ucs("A", "A")[:2])

print("2) unreachable goal on graph with a cycle (A -> Z), nothing may loop forever")
print("  BFS", bfs("A", "Z", cyc), "| DFS", dfs("A", "Z", cyc))
print("  DLS(limit 10)", dls("A", "Z", 10, cyc)[:2], " <- FAILURE: branch exhausted")
print("  DLS(limit 2) ", dls("A", "Z", 2, cyc)[:2], " <- CUTOFF only: NOT proof of unreachable")
print("  IDDFS(max 10)", iddfs("A", "Z", 10, cyc)[:3])

print("3) cycle but reachable goal (A -> D on cycle graph)")
print("  BFS", bfs("A", "D", cyc), "| DFS", dfs("A", "D", cyc), "| DLS(3)", dls("A", "D", 3, cyc)[:2])

print("4) negative weight is rejected by UCS")
bad = dict(wgraph); bad["A"] = [("B", -1), ("C", 5)]
try: ucs("A", "G", bad)
except ValueError as e: print("  ValueError:", e)
