import load_cell

# Ensure load_cell.start() was already called before this
fx = load_cell.lc._f[0]
fy = load_cell.lc._f[1]
fz = load_cell.lc._f[2]

mx = load_cell.lc._t[0]
my = load_cell.lc._t[1]
mz = load_cell.lc._t[2]

print("Forces:", fx, fy, fz)
print("Moments:", mx, my, mz)