# load_cell.py
# Copyright (c) 2025 Mohsen Khodaee

import time
from hardware import load_cell

load_cell.start()

# Wait until data is reasonably stable before zeroing
print("Waiting for data to stabilize...")
for _ in range(30):  # wait ~3 seconds with logging
    fx, fy, fz = load_cell.get_forces()
    mx, my, mz = load_cell.get_moments()
    print(f"PRE-ZERO Fx: {fx:.2f}, Fy: {fy:.2f}, Fz: {fz:.2f} | Mx: {mx:.2f}, My: {my:.2f}, Mz: {mz:.2f}")
    time.sleep(0.1)

# Now perform zeroing after stable readings
load_cell.zero()

print("Collecting data after zeroing...")
try:
    for _ in range(1000):
        fx, fy, fz = load_cell.get_forces()
        mx, my, mz = load_cell.get_moments()
        
        print(f"Fx: {fx:.2f} N, Fy: {fy:.2f} N, Fz: {fz:.2f} N")
        print(f"Mx: {mx:.2f} Nm, My: {my:.2f} Nm, Mz: {mz:.2f} Nm")
        print("-" * 40)
        time.sleep(0.1)
finally:
    load_cell.stop()
