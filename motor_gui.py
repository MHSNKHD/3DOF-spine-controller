# load_cell.py
# Copyright (c) 2025 Mohsen Khodaee

import tkinter as tk
from tkinter import ttk
import time
import hardware.motor as motor

# Initialize motor GPIO
motor.init()

# Duration options (in milliseconds)
durations = [50, 100, 150, 200]

def move_motor(axis, direction, duration_ms):
    print(f"Moving motor {axis} in direction {direction} for {duration_ms} ms")
    if direction == "P":
        motor.mot_pos(axis)
    else:
        motor.mot_neg(axis)

    time.sleep(duration_ms / 1000.0)  # Convert ms to seconds
    motor.mot_stop(axis)
    print(f"Motor {axis} stopped")

# GUI Setup
root = tk.Tk()
root.title("Motor Control GUI")

tk.Label(root, text="Select Duration (ms):").grid(row=0, column=1, pady=10)
duration_var = tk.IntVar(value=50)
duration_menu = ttk.Combobox(root, textvariable=duration_var, values=durations, width=10)
duration_menu.grid(row=0, column=2, pady=10)

axes = ["X", "Y", "Z"]
for i, axis in enumerate(axes, start=1):
    tk.Label(root, text=f"Motor {axis}").grid(row=i, column=0, padx=10)

    # Positive button
    btn_pos = tk.Button(root, text=f"{axis}+",
                        command=lambda a=axis: move_motor(a, "P", duration_var.get()))
    btn_pos.grid(row=i, column=1, padx=5, pady=5)

    # Negative button
    btn_neg = tk.Button(root, text=f"{axis}-",
                        command=lambda a=axis: move_motor(a, "N", duration_var.get()))
    btn_neg.grid(row=i, column=2, padx=5, pady=5)

# Start the GUI loop
root.mainloop()
