# Lab 2 - Intelligent Agents & the PEAS Framework

## Files
| File | Purpose |
|---|---|
| `lab2_percepts.py` | Reflex classroom agent and its 6-step percept/action trace (Section 2.5) |
| `lab2_model.py` | Stateful agent: remembers previous mode, returns (target, send_command) - Task 3 |
| `lab2_check.py` | Checks: reflex vs stateful, exact boundaries, noisy input around 26 C, optional hysteresis demo |
| `Lab2_Report.docx` | Report: both PEAS specs, classifications, comparison, full trace, failure analysis, reflection |
| `outputs/` | Captured console output of each script |

## Setup
Python 3.8+. Standard library only - nothing to install, no virtual environment.

## Run
```
python lab2_percepts.py
python lab2_model.py
python lab2_check.py
```
`lab2_model.py` and `lab2_check.py` import from `lab2_percepts.py`, so run them from inside this folder.

## Notes
- Temperatures are Celsius; ECO/COOL/WARM/IDLE are simulated labels, no hardware is controlled.
- Thresholds (20 and 26 C) come from the lab manual. The 25-26 C dead band in `lab2_check.py` is my own extra example, not part of the required task.
