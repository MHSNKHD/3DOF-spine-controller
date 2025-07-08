# motor.py
# Copyright (c) 2025 Mohsen Khodaee
from hardware import motor, load_cell

load_cell.start()
motor.init()

# Apply 20 N in Z
motor.apply_force("Z", 20)


