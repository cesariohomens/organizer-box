"""Compare two STLs by ray-casting a grid of lines through both.

The reference mesh is shifted by `--dz` so the two share a coordinate frame.
Reports how much solid length each ray sees and where the boundaries differ.
"""

import argparse

import numpy as np

from slices import Mesh


def clean(t):
    if t.size:
        t = t[np.concatenate(([True], np.diff(t) > 1e-6))]
    return t


def solid_len(t):
    return float(np.sum(t[1::2] - t[0::2])) if t.size >= 2 else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reference")
    ap.add_argument("candidate")
    ap.add_argument("--dz", type=float, default=0.0, help="shift applied to the reference")
    ap.add_argument("--step", type=float, default=4.0)
    ap.add_argument("--tol", type=float, default=0.15)
    args = ap.parse_args()

    ref = Mesh(args.reference)
    cand = Mesh(args.candidate)
    print(f"reference bbox {ref.lo} -> {ref.hi}")
    print(f"candidate bbox {cand.lo} -> {cand.hi}")
    print(f"reference bbox shifted by dz={args.dz}: z {ref.lo[2] + args.dz} -> {ref.hi[2] + args.dz}")

    shift = np.array([0.0, 0.0, args.dz])

    worst = []
    total_ref = total_cand = 0.0
    nrays = 0

    def compare(axis, a_vals, b_vals, label):
        nonlocal total_ref, total_cand, nrays
        for a in a_vals:
            for b in b_vals:
                # Reference is probed in its own frame; only z needs shifting.
                if axis == 2:
                    tr = clean(ref.profile(axis, a, b)) + args.dz
                elif axis == 0:
                    tr = clean(ref.profile(axis, a, b - args.dz))
                else:
                    tr = clean(ref.profile(axis, a, b - args.dz))
                tc = clean(cand.profile(axis, a, b))
                lr, lc = solid_len(tr), solid_len(tc)
                total_ref += lr
                total_cand += lc
                nrays += 1
                n = min(len(tr), len(tc))
                dmax = float(np.max(np.abs(tr[:n] - tc[:n]))) if n else 0.0
                if len(tr) != len(tc) or dmax > args.tol or abs(lr - lc) > args.tol:
                    worst.append((abs(lr - lc), dmax, label, a, b, len(tr), len(tc)))

    xs = np.arange(-46, 46.1, args.step) + 0.37
    ys = np.arange(-96, 96.1, args.step) + 0.53
    zs = np.arange(1, 63, args.step) + 0.29

    compare(2, xs, ys, "Z-ray")
    compare(0, ys, zs, "X-ray")
    compare(1, xs, zs, "Y-ray")

    print(f"\nrays: {nrays}")
    print(f"total solid length  reference={total_ref:.2f}  candidate={total_cand:.2f}  "
          f"delta={total_cand - total_ref:+.2f} ({100 * (total_cand - total_ref) / total_ref:+.3f}%)")
    print(f"rays flagged: {len(worst)}")
    worst.sort(reverse=True)
    for d, dmax, label, a, b, nr, nc in worst[:25]:
        print(f"  {label} a={a:8.2f} b={b:8.2f}  dlen={d:7.3f}  dmaxpos={dmax:7.3f}  "
              f"crossings ref={nr} cand={nc}")


if __name__ == "__main__":
    main()
