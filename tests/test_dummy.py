from hardware import load_cell
import time

load_cell.start()

for _ in range(10):
    fx, fy, fz = load_cell.get_forces()
    mx, my, mz = load_cell.get_moments()
    print(f"Fx: {fx:.2f} N, Fy: {fy:.2f} N, Fz: {fz:.2f} N")
    print(f"Mx: {mx:.2f} Nm, My: {my:.2f} Nm, Mz: {mz:.2f} Nm")
    print("---------------------")
    time.sleep(0.5)

load_cell.stop()