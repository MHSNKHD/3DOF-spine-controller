import tkinter as tk
from tkinter import ttk
import time
import hardware.motor as motor

# Initialize motor GPIO
motor.init()

# Updated duration options in milliseconds
durations = [10, 20, 30, 40, 50, 100, 150, 200, 250, 300]

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

# Duration selection dropdown
tk.Label(root, text="Select Duration (ms):").grid(row=0, column=1, columnspan=2, pady=10)
duration_var = tk.IntVar(value=50)
duration_menu = ttk.Combobox(root, textvariable=duration_var, values=durations, width=10, state="readonly")
duration_menu.grid(row=0, column=3, pady=10)

axes = ["X", "Y", "Z"]
for i, axis in enumerate(axes, start=1):
    tk.Label(root, text=f"Motor {axis}").grid(row=i, column=0, padx=10, pady=5)

    # Positive direction button
    btn_pos = tk.Button(root, text=f"{axis}+",
                        command=lambda a=axis, d="P": move_motor(a, d, duration_var.get()))
    btn_pos.grid(row=i, column=1, padx=5)

    # Negative direction button
    btn_neg = tk.Button(root, text=f"{axis}-",
                        command=lambda a=axis, d="N": move_motor(a, d, duration_var.get()))
    btn_neg.grid(row=i, column=2, padx=5)

# Run GUI loop
root.mainloop()
