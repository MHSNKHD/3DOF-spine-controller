# test_load_cell.py
# Copyright (c) 2025 Mohsen Khodaee, Oliver Wigger

import time
from hardware import load_cell

# === Step 1: Start the load cell ===
load_cell.start()

# === Step 2: Zero the load cell ===
print("Zeroing load cell... Do not apply any load.")
load_cell.zero()
print("Zeroing complete.")

# Cache offsets locally
fx0, fy0, fz0 = load_cell.cfg.LC0F
tx0, ty0, tz0 = load_cell.cfg.LC0T

# === Step 3: Read values ===
print("\nReading raw and corrected force/moment data:\n")

for _ in range(100):
    fx, fy, fz = load_cell.lc._f  # already corrected
    mx, my, mz = load_cell.lc._t

    print(f"Forces (N): Fx={fx:.2f}, Fy={fy:.2f}, Fz={fz:.2f}")
    print(f"Moments (Nm): Mx={mx:.3f}, My={my:.3f}, Mz={mz:.3f}")
    print("-" * 60)
    time.sleep(0.5)

# === Step 4: Stop the load cell ===
load_cell.stop()
print("Load cell stopped.")
