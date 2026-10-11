# Lab 4 - Informed Search: Heuristics & A* 

# Files
| File | Purpose |
|---|---|
| `lab4_astar_audit.py` | Supplied A* + traced version, heuristic audit (admissibility/consistency), A* vs UCS (h=0) comparison, h(C)=10 experiment |
| `lab4_check.py` | Extra checks: start==goal, unreachable goal, harmless overestimate h(B)=10, stale-entry demo |
| `Lab4_Report.docx` | Report with manual g/h/f work, audit, comparison table, overestimate experiment, reflection |
| `outputs/` | Captured console output of both scripts |

# Setup
Python 3.8+, standard library only. No installs or virtual environment.

# Run (from inside this folder)
```
python lab4_astar_audit.py
python lab4_check.py
```

# Conventions
- Queue entries are `(f, g, node, path)`; ties break by smaller g, then node name.
- "Expanded" = successors examined. The goal is processed but not counted. Stale entries are skipped and counted separately.
- Edge weights and h values are abstract time units from the manual, not measured distances.
