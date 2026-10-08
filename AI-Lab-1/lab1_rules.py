# Lab 1 - Task 2: transparent rule-based scholarship pre-screen.

# Retained conditions : score >= 70 ; documents complete
# New named conditions: attendance_ok  (attendance >= 75 %)
#                       no_disciplinary_flag (no active disciplinary record)

# ASSUMPTION: every threshold below is a SYNTHETIC lab assumption, not real policy.
# 'Review' only means 'send to a human reviewer' - it is NOT an award decision.

MIN_SCORE = 70          # synthetic
MIN_ATTENDANCE = 75     # synthetic (percent)

def screen(score, documents_complete, attendance, disciplinary_flag):
    # Return (decision, reason). Every failed rule is named explicitly.
    failed = []
    if score < MIN_SCORE:
        failed.append(f"score {score} < {MIN_SCORE}")
    if not documents_complete:
        failed.append("documents incomplete")
    if attendance < MIN_ATTENDANCE:
        failed.append(f"attendance_ok failed ({attendance}% < {MIN_ATTENDANCE}%)")
    if disciplinary_flag:
        failed.append("no_disciplinary_flag failed (active record)")
    if failed:
        return "Hold", "; ".join(failed)
    return "Review", "all four conditions satisfied"

# Exactly four core tests: (id, score, complete, attendance, flag, expected, purpose)
TESTS = [
    ("T1_pass",             85, True, 90, False, "Review", "all conditions satisfied"),
    ("T2_low_attendance",   85, True, 60, False, "Hold",   "fails ONLY attendance_ok"),
    ("T3_disciplinary",     85, True, 90, True,  "Hold",   "fails ONLY no_disciplinary_flag"),
    ("T4_boundary",         70, True, 75, False, "Review", "exact thresholds (>= is inclusive)"),
]

if __name__ == "__main__":
    print("NOTE: thresholds are synthetic lab assumptions.\n")
    ok = 0
    for tid, s, c, att, flag, expected, purpose in TESTS:
        actual, reason = screen(s, c, att, flag)
        status = "PASS" if actual == expected else "FAIL"
        ok += status == "PASS"
        print(f"{tid}: input(score={s}, complete={c}, attendance={att}, disciplinary={flag})")
        print(f"   purpose  : {purpose}")
        print(f"   expected : {expected}")
        print(f"   actual   : {actual}   [{status}]")
        print(f"   reason   : {reason}")
    print(f"{ok}/{len(TESTS)} tests passed")
