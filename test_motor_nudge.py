# load_cell.py
# Copyright (c) 2025 Mohsen Khodaee

import time
import motor  # Assuming your motor control functions are in motor.py

# Initialize GPIO and motor pins
motor.init()

# Nudge motor X forward very briefly
print("Nudging motor X in positive direction...")
motor.mot_pos("X")
time.sleep(0.05)  # run for 50 milliseconds (adjust for longer or shorter movement)
motor.mot_stop("X")
print("Motor X stopped.")
