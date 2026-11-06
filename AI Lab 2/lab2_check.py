# Lab 2 - checks and noisy-sequence test

import lab2_model
from lab2_model import StatefulClassroomAgent

a = StatefulClassroomAgent()
assert a.act(29, True) == ("COOL", True)
assert a.act(29, True) == ("COOL", False)   
assert a.act(20, True) == ("IDLE", True)    
assert a.act(26, True) == ("IDLE", False)   
assert a.act(19, True) == ("WARM", True)
assert a.act(29, False) == ("ECO", True)    
assert a.act(29, False) == ("ECO", False)
print("All checks passed")

print()
print("Noisy test around 26C")
b = StatefulClassroomAgent()
commands = 0
for temp in [25.9, 26.1, 25.9, 26.1, 25.9, 26.1]:
    prev = b.previous_mode
    target, send = b.act(temp, True)
    commands += send
    print("prev", prev, " temp", temp, " target", target , "SEND" if send else "no command")
print("Commands sent:", commands, "out of 6 readings")
