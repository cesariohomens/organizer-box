"""Inspect a binary STL: bounding box, Z levels and XY cross-section slices.

Used to reverse-engineer the geometry of an existing organizer box.
"""

import struct
import sys

import numpy as np


def load_binary_stl(path):
    """Load an STL, binary or ASCII, as (normals, triangles)."""
    with open(path, "rb") as fh:
        data = fh.read()

    if data[:5].lower() == b"solid" and len(data) >= 84:
        count = struct.unpack("<I", data[80:84])[0]
        if 84 + count * 50 != len(data):
            return load_ascii_stl(data)
    count = struct.unpack("<I", data[80:84])[0]
    raw = np.frombuffer(data, dtype=np.uint8, count=count * 50, offset=84)
    raw = raw.reshape(count, 50)
    floats = raw[:, :48].copy().view("<f4").reshape(count, 4, 3)
    normals = floats[:, 0, :]
    tris = floats[:, 1:, :]
    return normals, tris


def load_ascii_stl(data):
    normals = []
    verts = []
    for line in data.decode("ascii", "replace").splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "facet" and len(parts) >= 5:
            normals.append([float(v) for v in parts[2:5]])
        elif parts[0] == "vertex" and len(parts) >= 4:
            verts.append([float(v) for v in parts[1:4]])
    tris = np.array(verts, dtype=np.float32).reshape(-1, 3, 3)
    return np.array(normals, dtype=np.float32), tris


def slice_occupancy(tris, z, grid_x, grid_y):
    """Ray-cast along +Z from each (x, y) sample at height z; odd hits = inside."""
    v0, v1, v2 = tris[:, 0], tris[:, 1], tris[:, 2]
    inside = np.zeros((grid_y.size, grid_x.size), dtype=bool)
    for iy, y in enumerate(grid_y):
        for ix, x in enumerate(grid_x):
            hits = ray_hits(v0, v1, v2, x, y, z)
            inside[iy, ix] = hits % 2 == 1
    return inside


def ray_hits(v0, v1, v2, x, y, z):
    """Count triangles crossed by the ray (x, y, z) -> +Z, Moller-Trumbore."""
    edge1 = v1 - v0
    edge2 = v2 - v0
    direction = np.array([0.0, 0.0, 1.0], dtype=np.float32)
    h = np.cross(direction, edge2)
    a = np.einsum("ij,ij->i", edge1, h)
    mask = np.abs(a) > 1e-9
    f = np.zeros_like(a)
    f[mask] = 1.0 / a[mask]
    s = np.array([x, y, z], dtype=np.float32) - v0
    u = f * np.einsum("ij,ij->i", s, h)
    q = np.cross(s, edge1)
    v = f * np.einsum("j,ij->i", direction, q)
    t = f * np.einsum("ij,ij->i", edge2, q)
    ok = mask & (u >= 0) & (u <= 1) & (v >= 0) & (u + v <= 1) & (t > 1e-6)
    return int(np.count_nonzero(ok))


def runs(mask, coords):
    """Return [(start, end, filled)] runs over a boolean profile."""
    out = []
    start = 0
    for i in range(1, mask.size + 1):
        if i == mask.size or mask[i] != mask[start]:
            out.append((coords[start], coords[i - 1], bool(mask[start])))
            start = i
    return out


def main(path):
    normals, tris = load_binary_stl(path)
    pts = tris.reshape(-1, 3)
    lo, hi = pts.min(axis=0), pts.max(axis=0)
    print(f"triangles: {len(tris)}")
    print(f"bbox min : {lo}")
    print(f"bbox max : {hi}")
    print(f"size     : {hi - lo}")

    zs = np.unique(np.round(pts[:, 2], 3))
    print(f"\ndistinct Z levels ({zs.size}): {zs[:40]}")
    xs = np.unique(np.round(pts[:, 0], 3))
    ys = np.unique(np.round(pts[:, 1], 3))
    print(f"distinct X ({xs.size}): {xs[:60]}")
    print(f"distinct Y ({ys.size}): {ys[:60]}")

    # Horizontal profile at a height that is above the floor but below the rim.
    z_probe = lo[2] + (hi[2] - lo[2]) * 0.75
    step = 0.25
    gx = np.arange(lo[0] + step / 2, hi[0], step)
    y_mid = (lo[1] + hi[1]) / 2
    profile_x = np.array(
        [ray_hits(tris[:, 0], tris[:, 1], tris[:, 2], x, y_mid, z_probe) % 2 == 1 for x in gx]
    )
    print(f"\nX runs at y={y_mid:.2f}, z={z_probe:.2f} (solid=wall):")
    for a, b, filled in runs(profile_x, gx):
        print(f"  {'WALL' if filled else 'open'} {a:8.2f} -> {b:8.2f}  width {b - a + step:6.2f}")

    gy = np.arange(lo[1] + step / 2, hi[1], step)
    x_mid = (lo[0] + hi[0]) / 2
    profile_y = np.array(
        [ray_hits(tris[:, 0], tris[:, 1], tris[:, 2], x_mid, y, z_probe) % 2 == 1 for y in gy]
    )
    print(f"\nY runs at x={x_mid:.2f}, z={z_probe:.2f} (solid=wall):")
    for a, b, filled in runs(profile_y, gy):
        print(f"  {'WALL' if filled else 'open'} {a:8.2f} -> {b:8.2f}  width {b - a + step:6.2f}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/home/cesario/Downloads/200x100_4_V2.stl")
