# read_load_cell_directly.py
# Example usage of load_cell without calling get_forces() or get_moments()

import time
from hardware import load_cell

# === Step 1: Start the load cell ===
load_cell.start()

# Optional: Zero the load cell to remove offsets (recommended if unloaded)
load_cell.zero()

# === Step 2: Read values directly ===
print("\nReading force and moment data directly (without get_forces/get_moments):\n")

try:
    for _ in range(10):  # Read 10 times
        fx = load_cell.lc._f[0]
        fy = load_cell.lc._f[1]
        fz = load_cell.lc._f[2]

        mx = load_cell.lc._t[0]
        my = load_cell.lc._t[1]
        mz = load_cell.lc._t[2]

        print(f"Forces (N): Fx={fx:.2f}, Fy={fy:.2f}, Fz={fz:.2f}")
        print(f"Moments (Nm): Mx={mx:.3f}, My={my:.3f}, Mz={mz:.3f}")
        print("-" * 50)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Interrupted by user.")

# === Step 3: Stop the load cell ===
load_cell.stop()
print("Load cell stopped.")
