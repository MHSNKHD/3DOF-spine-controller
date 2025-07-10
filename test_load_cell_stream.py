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

try:
    for _ in range(100):
        # Raw sensor readings
        raw_fx = load_cell.lc._f[0]
        raw_fy = load_cell.lc._f[1]
        raw_fz = load_cell.lc._f[2]

        raw_mx = load_cell.lc._t[0]
        raw_my = load_cell.lc._t[1]
        raw_mz = load_cell.lc._t[2]

        # Corrected values
        fx = raw_fx - fx0
        fy = raw_fy - fy0
        fz = raw_fz - fz0

        mx = raw_mx - tx0
        my = raw_my - ty0
        mz = raw_mz - tz0

        # Print both raw and corrected
        print(f"RAW Forces (N): Fx={raw_fx:.2f}, Fy={raw_fy:.2f}, Fz={raw_fz:.2f}")
        print(f"RAW Moments (Nm): Mx={raw_mx:.3f}, My={raw_my:.3f}, Mz={raw_mz:.3f}")

        print(f"CORR Forces (N): Fx={fx:.2f}, Fy={fy:.2f}, Fz={fz:.2f}")
        print(f"CORR Moments (Nm): Mx={mx:.3f}, My={my:.3f}, Mz={mz:.3f}")
        print("-" * 60)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Interrupted by user.")

# === Step 4: Stop the load cell ===
load_cell.stop()
print("Load cell stopped.")
