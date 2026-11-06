# Lab 1 
# Task 2: rule-based scholarship screening with 2 extra conditions

def screen(score, docs_complete, attendance, has_recommendation):
    if score < 70:
        return "Hold", "score below 70"
    if not docs_complete:
        return "Hold", "documents incomplete"
    if attendance < 75:                      
        return "Hold", "attendance below 75%"
    if not has_recommendation:               
        return "Hold", "recommendation letter missing"
    return "Review", "all conditions met"

tests = [
    ("pass",            (85, True, 90, True), "Review"),
    ("low_attendance",  (85, True, 60, True), "Hold"),
    ("no_letter",       (85, True, 90, False), "Hold"),
    ("boundary",        (70, True, 75, True), "Review"),
]

for name, inputs, expected in tests:
    actual, reason = screen(*inputs)
    status = "PASS" if actual == expected else "FAIL"
    print("Test:", name)
    print("  input    (score, docs, attendance, letter):", inputs)
    print("  expected:", expected)
    print("  actual  :", actual)
    print("  reason  :", reason)
    print("  result  :", status)
    print()
