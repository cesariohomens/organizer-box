"""Render ASCII cross-sections of a binary STL along the three axes."""

import sys

import numpy as np

from inspect_stl import load_binary_stl


class Mesh:
    def __init__(self, path):
        _, tris = load_binary_stl(path)
        self.tris = tris.astype(np.float64)
        pts = self.tris.reshape(-1, 3)
        self.lo = pts.min(axis=0)
        self.hi = pts.max(axis=0)

    def crossings(self, axis, a, b):
        """Sorted coordinates where the line parallel to `axis` through (a, b) hits the mesh."""
        v0, v1, v2 = self.tris[:, 0], self.tris[:, 1], self.tris[:, 2]
        d = np.zeros(3)
        d[axis] = 1.0
        origin = np.zeros(3)
        others = [i for i in range(3) if i != axis]
        origin[others[0]] = a
        origin[others[1]] = b

        edge1 = v1 - v0
        edge2 = v2 - v0
        h = np.cross(d, edge2)
        det = np.einsum("ij,ij->i", edge1, h)
        mask = np.abs(det) > 1e-12
        f = np.zeros_like(det)
        f[mask] = 1.0 / det[mask]
        s = origin - v0
        u = f * np.einsum("ij,ij->i", s, h)
        q = np.cross(s, edge1)
        v = f * np.einsum("j,ij->i", d, q)
        t = f * np.einsum("ij,ij->i", edge2, q)
        ok = mask & (u >= 0) & (u <= 1) & (v >= 0) & (u + v <= 1)
        return np.sort(t[ok])

    def inside(self, axis, a, b, coord):
        t = self.crossings(axis, a, b)
        # Collapse duplicates from shared edges / coincident facets.
        if t.size:
            t = t[np.concatenate(([True], np.diff(t) > 1e-6))]
        return int(np.count_nonzero(t > coord)) % 2 == 1

    def profile(self, axis, a, b):
        t = self.crossings(axis, a, b)
        if t.size:
            t = t[np.concatenate(([True], np.diff(t) > 1e-6))]
        return t


def spans(t):
    """Turn a sorted crossing list into solid [start, end] intervals."""
    return [(t[i], t[i + 1]) for i in range(0, len(t) - 1, 2)]


def ascii_slice(mesh, axis, coord, cols=100):
    """Print a filled/empty map of the plane perpendicular to `axis` at `coord`."""
    others = [i for i in range(3) if i != axis]
    a0, a1 = mesh.lo[others[0]], mesh.hi[others[0]]
    b0, b1 = mesh.lo[others[1]], mesh.hi[others[1]]
    step = (a1 - a0) / cols
    rows = max(4, int((b1 - b0) / step / 2))
    names = "XYZ"
    print(f"\n=== slice {names[axis]}={coord:g}  ({names[others[0]]} horiz, {names[others[1]]} vert) ===")
    for r in range(rows):
        b = b1 - (r + 0.5) * (b1 - b0) / rows
        line = []
        for c in range(cols):
            a = a0 + (c + 0.5) * (a1 - a0) / cols
            line.append("#" if mesh.inside(axis, a, b, coord) else ".")
        print("".join(line))


def main():
    path = sys.argv[1]
    mesh = Mesh(path)
    print(f"bbox {mesh.lo} -> {mesh.hi}  size {mesh.hi - mesh.lo}")

    for z in [-33.0, -31.0, -29.0, -20.0, 0.0, 8.0, 13.0, 25.0, 29.0]:
        ascii_slice(mesh, 2, z, cols=100)

    print("\n\n=== vertical Z profiles (solid spans) ===")
    for x, y in [(-49.0, 0.0), (0.0, -99.0), (0.0, 0.0), (-45.0, 0.0), (-49.0, -95.0), (0.0, -50.0)]:
        sp = spans(mesh.profile(2, x, y))
        pretty = ", ".join(f"[{a:.2f},{b:.2f}]" for a, b in sp)
        print(f"x={x:7.2f} y={y:7.2f}: {pretty}")

    print("\n=== horizontal X profiles ===")
    for y, z in [(0.0, 27.0), (0.0, 8.0), (0.0, 3.0), (-95.0, 8.0)]:
        sp = spans(mesh.profile(0, y, z))
        pretty = ", ".join(f"[{a:.2f},{b:.2f}]" for a, b in sp)
        print(f"y={y:7.2f} z={z:7.2f}: {pretty}")

    print("\n=== horizontal Y profiles ===")
    for x, z in [(0.0, 27.0), (0.0, 8.0), (0.0, 3.0), (-49.0, 8.0), (-49.0, 3.0)]:
        sp = spans(mesh.profile(1, x, z))
        pretty = ", ".join(f"[{a:.2f},{b:.2f}]" for a, b in sp)
        print(f"x={x:7.2f} z={z:7.2f}: {pretty}")


if __name__ == "__main__":
    main()
