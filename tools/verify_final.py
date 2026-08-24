"""Check the produced box against the intended dimensions."""

import sys

import numpy as np

from slices import Mesh

STL = sys.argv[1] if len(sys.argv) > 1 else "../organizer_box_100x200x64_rib1.33.stl"
mesh = Mesh(STL)


def clean(t):
    if t.size:
        t = t[np.concatenate(([True], np.diff(t) > 1e-6))]
    return t


print(f"bbox {mesh.lo} -> {mesh.hi}   size {mesh.hi - mesh.lo}")

print("\nZ crossings through the long wall at x=-48.5, y=0 (even column):")
t = clean(mesh.profile(2, -48.5, 0.0))
print(f"  {np.round(t, 3)}")
solid = [(t[i], t[i + 1]) for i in range(0, len(t) - 1, 2)]
print("  ribs (solid runs): " + ", ".join(f"{b - a:.3f}" for a, b in solid))

print("\nZ crossings at x=-48.5, y=8.660 (odd column):")
t = clean(mesh.profile(2, -48.5, 8.6603))
print(f"  {np.round(t, 3)}")

print("\nY crossings at x=-48.5, z=42 (mid height of an even-column cell):")
t = clean(mesh.profile(1, -48.5, 42.0))
print(f"  {np.round(t[:14], 3)}")
print(f"  hole width across corners: {t[len(t)//2] - t[len(t)//2 - 1]:.4f}")

print("\nX crossings at y=0, z=60 (solid rim) and y=8.66, z=42:")
print(f"  z=60: {np.round(clean(mesh.profile(0, 0.0, 60.0)), 3)}")
print(f"  y=8.66,z=42: {np.round(clean(mesh.profile(0, 8.6603, 42.0)), 3)}")

print("\nFloor and rim:")
print(f"  centre column x=0,y=0: {np.round(clean(mesh.profile(2, 0.0, 0.0)), 3)}")
print(f"  x=0,y=90 : {np.round(clean(mesh.profile(2, 0.0, 90.0)), 3)}")

print("\nShort wall, Z crossings at x=0, y=-98.5:")
print(f"  {np.round(clean(mesh.profile(2, 0.0, -98.5)), 3)}")
print("Short wall, X crossings at y=-98.5, z=42:")
print(f"  {np.round(clean(mesh.profile(0, -98.5, 42.0)), 3)}")

print("\nMinimum material between holes (scan of solid run widths along z at several columns):")
for y in [0.0, 8.6603, 17.3205, 4.3301]:
    t = clean(mesh.profile(2, -48.5, y))
    runs = [t[i + 1] - t[i] for i in range(0, len(t) - 1, 2)]
    print(f"  y={y:8.3f}: " + ", ".join(f"{r:.3f}" for r in runs))
