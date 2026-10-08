# Lab 1 - Introduction to AI & Paradigms


## Contents
| File | Purpose |
|---|---|
| `lab1_compare.py` | Section 1.5: symbolic rule vs probability threshold on 4 cases |
| `lab1_isolate.py` | Section 1.6: changes boundary score / probability one at a time |
| `lab1_rules.py` | Task 2: rule system with 2 extra named conditions + 4 core tests |
| `Lab1_Report.docx` | Full report (timeline, tests, disagreement table, comparison, reflection) |
| `outputs/` | Captured console output of every script |

## Setup
Python 3.8+ only. No external packages, no virtual environment needed.

## Run
```
python lab1_compare.py
python lab1_isolate.py
python lab1_rules.py
```
To regenerate captured outputs: `python lab1_rules.py > outputs/lab1_rules_output.txt` (same for the others).

## Notes
- All thresholds (score >= 70, attendance >= 75, p >= 0.70) and probabilities are **synthetic lab assumptions**.
- No model is trained; the probability branch is a behaviour comparison, not an accuracy experiment.
- No credentials or private data are included.
