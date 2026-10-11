# Lab 2 - Section 2.5: reflex smart-classroom agent and its percept/action trace.
# Temperature is in degrees Celsius; ECO/COOL/WARM/IDLE are simulated mode labels
# (no hardware is controlled). An empty room has priority over temperature.

class ClassroomAgent:
    def act(self, temp, occupied):
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"

PERCEPTS = [(29, True), (29, True), (20, True),
            (26, True), (19, True), (29, False)]

if __name__ == "__main__":
    agent = ClassroomAgent()
    for step, percept in enumerate(PERCEPTS, 1):
        print(step, percept, "target mode", agent.act(*percept))
