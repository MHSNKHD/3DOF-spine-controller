# motor.py
# Copyright (c) 2025 Mohsen Khodaee
from hardware import motor, load_cell

load_cell.start()
motor.init()

# Apply 200 N in X
motor.apply_force("X", 20)

# Apply 2 Nm around Z
motor.apply_moment("Z", 1.0)


