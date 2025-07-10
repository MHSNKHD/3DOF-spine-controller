# load_cell.py
# Copyright (c) 2025 Mohsen Khodaee

import time
from hardware import load_cell

load_cell.start()
time.sleep(3)
load_cell.zero()
time.sleep(3)

try:
    for _ in range(1000):  # print 20 samples
        fx, fy, fz = load_cell.get_forces()
        mx, my, mz = load_cell.get_moments()
        
        print(f"Fx: {fx:.2f} N, Fy: {fy:.2f} N, Fz: {fz:.2f} N")
        print(f"Mx: {mx:.2f} Nm, My: {my:.2f} Nm, Mz: {mz:.2f} Nm")
        print("-" * 40)
        
        time.sleep(0.1)  # 10 Hz
finally:
    load_cell.stop()
