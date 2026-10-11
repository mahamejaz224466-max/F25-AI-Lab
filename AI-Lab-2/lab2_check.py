# Lab 2 - checks: reflex vs stateful comparison, boundaries, and the noisy
# sequence around 26 C (Section 2.7). Uses plain asserts; prints a summary.

from lab2_percepts import ClassroomAgent, PERCEPTS
from lab2_model import StatefulClassroomAgent, TRACE_PERCEPTS

# 1. Stateful agent must pick the SAME target as the reflex agent every time.
reflex, stateful = ClassroomAgent(), StatefulClassroomAgent()
for p in TRACE_PERCEPTS:
    assert reflex.act(*p) == stateful.act(*p)[0], p
print("check 1 OK: stateful targets == reflex targets on all 8 percepts")

# 2. Exact boundaries are IDLE for an occupied room (< and > are strict).
a = ClassroomAgent()
assert a.act(20, True) == "IDLE" and a.act(26, True) == "IDLE"
assert a.act(19.9, True) == "WARM" and a.act(26.1, True) == "COOL"
print("check 2 OK: 20 and 26 are IDLE; 19.9 -> WARM; 26.1 -> COOL")

# 3. Command counts: reflex re-sends every step, stateful only on change.
reflex_cmds = len(TRACE_PERCEPTS)
s = StatefulClassroomAgent()
stateful_cmds = sum(s.act(*p)[1] for p in TRACE_PERCEPTS)
print(f"check 3: reflex sends {reflex_cmds} commands, stateful sends {stateful_cmds}")

# 4. Noisy sensor around 26 C: memory alone does NOT stop flapping.
noisy = [25.9, 26.1, 25.9, 26.1, 25.9, 26.1]
s = StatefulClassroomAgent()
print("\ncheck 4: noisy sequence around 26 C (stateful agent, no hysteresis)")
print("step | previous | temp | target | command")
n_sent = 0
for i, t in enumerate(noisy, 1):
    prev = s.previous_mode
    target, send = s.act(t, True)
    n_sent += send
    print(i, prev, t, target, "SEND" if send else "no command", sep=" | ")
print(f"commands sent: {n_sent} of {len(noisy)}  -> flapping IDLE/COOL")

# 5. PROPOSED improvement (extra, NOT part of the required task): hysteresis.
#    Start cooling above 26, but only stop once temp falls below 25.
class HysteresisAgent(StatefulClassroomAgent):
    def act(self, temp, occupied):
        if occupied and self.previous_mode == "COOL" and 25 <= temp <= 26:
            return "COOL", False          # keep cooling inside the dead band
        return super().act(temp, occupied)

h = HysteresisAgent()
h_sent = sum(h.act(t, True)[1] for t in noisy)
print(f"\ncheck 5: with a 25-26 C dead band the same noise sends {h_sent} command(s)")
