"""Fit a superellipse exponent to the outer and inner corner outlines."""

import numpy as np
from scipy.optimize import least_squares

from slices import Mesh

mesh = Mesh("/home/cesario/Downloads/200x100_4_V2.stl")
Z = 26.0


def clean(t):
    if t.size:
        t = t[np.concatenate(([True], np.diff(t) > 1e-6))]
    return t


outer, inner = [], []
for y in np.arange(-99.8, -85.0, 0.1):
    t = clean(mesh.profile(0, y, Z))
    neg = t[t < 0]
    if neg.size >= 2:
        outer.append((neg[0], y))
        inner.append((neg[-1], y))
for x in np.arange(-49.8, -35.0, 0.1):
    t = clean(mesh.profile(1, x, Z))
    neg = t[t < 0]
    if neg.size >= 2:
        outer.append((x, neg[0]))
        inner.append((x, neg[-1]))


def fit(points, cx, cy, label, xmin, ymin):
    # Keep only the curved quadrant, dropping the tangent straight runs at both ends.
    pts = np.array(
        [
            (x, y)
            for x, y in points
            if x <= cx - 0.05 and y <= cy - 0.05 and x >= xmin + 0.15 and y >= ymin + 0.15
        ]
    )

    def resid(params):
        n, r = params
        u = np.abs((pts[:, 0] - cx) / r)
        v = np.abs((pts[:, 1] - cy) / r)
        return u**n + v**n - 1.0

    sol = least_squares(resid, [2.4, 10.0])
    n, r = sol.x
    # Convert implicit residual into an approximate radial distance error.
    err = np.abs(resid(sol.x))
    print(f"{label}: n={n:.4f}  r={r:.4f}  pts={len(pts)}  max|f|={err.max():.5f}  rms={np.sqrt((err**2).mean()):.5f}")
    return n, r


print("Corner reference points: outer center (-40, -90), inner center (-37, -87)")
fit(outer, -40.0, -90.0, "OUTER", -50.0, -100.0)
fit(inner, -37.0, -87.0, "INNER", -47.0, -97.0)

print("\nCheck a few outer points against n=2.4, r=10:")
for x, y in outer[::20]:
    u, v = abs((x + 40) / 10), abs((y + 90) / 10)
    print(f"  ({x:8.3f},{y:8.3f})  u^n+v^n = {u**2.4 + v**2.4:.4f}")
