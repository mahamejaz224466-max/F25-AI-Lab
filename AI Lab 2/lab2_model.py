# Lab 2 - Task 3: stateful classroom agent (remembers previous mode)

class StatefulClassroomAgent:
    def __init__(self):
        self.previous_mode = None      

    def target_mode(self, temp, occupied):
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"

    def act(self, temp, occupied):
        target = self.target_mode(temp, occupied)
        send = target != self.previous_mode
        self.previous_mode = target
        return target, send


if __name__ == "__main__":
    agent = StatefulClassroomAgent()
    percepts = [
        (29, True),    
        (29, True),    
        (20, True),    
        (26, True),    
        (19, True),    
        (29, False),   
        (29, False),   
    ]
    print("step    previous mode    percept    target    command")
    for step, percept in enumerate(percepts, 1):
        prev = agent.previous_mode
        target, send = agent.act(*percept)
        outcome = "SEND" if send else "no command"
        print(step, prev, percept, target, outcome )
