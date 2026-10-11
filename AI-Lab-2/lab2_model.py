# Lab 2 - Task 3: stateful classroom agent.
# Same thresholds and occupancy priority as the reflex agent, plus ONE piece of
# internal storage (previous target mode). act() returns (target, send_command):
# send_command is True only when the target differs from the previous one.
# NOTE: this is memory, not learning, and not hysteresis (see lab2_check.py).

from lab2_percepts import ClassroomAgent

class StatefulClassroomAgent:
    def __init__(self):
        self.previous_mode = None          # nothing sent yet
        self._policy = ClassroomAgent()    # reuse the unchanged reflex policy

    def act(self, temp, occupied):
        target = self._policy.act(temp, occupied)
        send = target != self.previous_mode
        self.previous_mode = target
        return target, send

TRACE_PERCEPTS = [
    (29, True),    # first cooling request
    (29, True),    # repeated percept
    (20, True),    # exact lower boundary
    (26, True),    # exact upper boundary
    (19, True),    # mode transition IDLE -> WARM
    (29, False),   # empty room (occupancy priority)
    (22, False),   # empty room again (repeat)
    (22, True),    # room occupied again, comfortable
]

if __name__ == "__main__":
    agent = StatefulClassroomAgent()
    print("step | previous | percept | target | command")
    sent = 0
    for step, (t, occ) in enumerate(TRACE_PERCEPTS, 1):
        prev = agent.previous_mode
        target, send = agent.act(t, occ)
        sent += send
        print(step, prev, (t, occ), target, "SEND" if send else "no command", sep=" | ")
    print(f"commands sent: {sent} of {len(TRACE_PERCEPTS)} percepts")
