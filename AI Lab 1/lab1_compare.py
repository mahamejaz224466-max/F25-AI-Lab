# Lab 1 - Rule-based vs threshold comparison 

def symbolic(score, complete):
    return "Review" if complete and score >= 70 else "Hold"

def threshold(probability):
    return "Review" if probability >= 0.70 else "Hold"

cases = [
    ("complete_high", 82, True, 0.81),
    ("complete_low", 68, True, 0.74),
    ("incomplete_high", 91, False, 0.88),
    ("boundary", 70, True, 0.70),
]

print("case    symbolic    threshold     disagreement")
for name, score, complete, probability in cases:
    a = symbolic(score, complete)
    b = threshold(probability)
    print(name, a, b, a != b )

print()
print("Boundary experiment")
print("score 69, complete  ", symbolic(69, True))
print("probability 0.69   ", threshold(0.69))
