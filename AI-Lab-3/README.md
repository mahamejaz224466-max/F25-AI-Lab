# Lab 3 - Uninformed Search: BFS, DFS, DLS, IDDFS & UCS

## Files
| File | Purpose |
|---|---|
| `lab3_bfs_dfs.py` | Supplied BFS/DFS + step-by-step trace versions (Task 1), verified against the supplied code |
| `lab3_depth_search.py` | DLS and IDDFS with FOUND / CUTOFF / FAILURE and path-local cycle check (Task 2) |
| `lab3_ucs.py` | Weighted graph (with added C->G corridor), UCS, independent cost check, BFS comparison (Task 3) |
| `lab3_check.py` | Edge cases: start == goal, unreachable goal, cycle, negative weight |
| `Lab3_Report.docx` | Report with traces, results, comparison, edge-case analysis, reflection |
| `outputs/` | Captured console output of every script |

## Setup
Python 3.8+, standard library only. No virtual environment or installs needed.

## Run (from inside this folder)
```
python lab3_bfs_dfs.py
python lab3_depth_search.py
python lab3_ucs.py
python lab3_check.py
```

## Notes
- Successor-list order is the tie-breaking order. Depth counts edges (A = depth 0).
- Node counts include the goal when it is processed.
- Edge weights in `lab3_ucs.py` are my own choice, picked to match the manual's stated results (BFS cost 12, UCS cost 3). Swap in the instructor's table if one is supplied.
