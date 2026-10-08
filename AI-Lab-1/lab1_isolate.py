# Lab 1 - Section 1.6: isolate the effect of the boundary score and probability.
# Changes ONE input at a time on the 'boundary' case (score 70, complete, p=0.70).
from lab1_compare import symbolic, threshold

runs = [
    ("baseline",             70, True, 0.70),
    ("score 70 -> 69 only",  69, True, 0.70),
    ("prob 0.70 -> 0.69 only", 70, True, 0.69),
    ("both lowered",         69, True, 0.69),
]
print("run | symbolic | threshold | disagreement")
for name, score, complete, p in runs:
    a, b = symbolic(score, complete), threshold(p)
    print(name, a, b, a != b, sep=" | ")
