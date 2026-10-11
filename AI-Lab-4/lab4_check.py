# Lab 4 - extra checks: stale entries, start==goal, unreachable goal, and an
# overestimate that does NOT change the answer (so one unchanged run proves nothing).

from lab4_astar_audit import astar, astar_trace, path_cost, graph, H

print("1) start == goal:", astar(graph, H, "S", "S"))

print("2) unreachable goal (no edge into Z):", end=" ")
g2 = dict(graph); g2["Z"] = []; H2 = dict(H); H2["Z"] = 0
print(astar(g2, H2, "S", "Z"))

print("3) overestimate on a DIFFERENT node: h(B) 4 -> 10 (true remaining cost of B = 5)")
Hb = dict(H); Hb["B"] = 10
cost, path, log, exp, stale = astar_trace(graph, Hb, "S", "G")
print("   result:", cost, "->".join(path), "| expanded:", exp,
      "| same as the original answer (cost 6):", cost == 6)

print("4) stale queue entry demo (h = 0). S->A=4, S->B=1, B->A=2, A->G=1")
gs = {"S": [("A", 4), ("B", 1)], "A": [("G", 1)], "B": [("A", 2)], "G": []}
H0 = {n: 0 for n in gs}
cost, path, log, exp, stale = astar_trace(gs, H0, "S", "G")
for i, e in enumerate(log, 1):
    print("  ", i, e["node"], "g=", e["g"], e["status"])
print("   path", "->".join(path), "cost", cost, "| independent", path_cost(gs, path),
      "| expanded", exp, "| stale skipped", stale)
