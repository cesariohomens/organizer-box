#!/usr/bin/env python3
"""Copy the OpenSCAD model into the <script id="scad-source"> block of the web
app, so the .scad the page hands out is always the one in this repository."""

import re
import sys
from pathlib import Path

BLOCK = re.compile(
    r'(<script id="scad-source" type="text/plain">\n).*?(</script>)',
    re.DOTALL,
)


def main():
    root = Path(__file__).resolve().parent.parent
    scad = (root / (sys.argv[1] if len(sys.argv) > 1 else "organizer_box.scad")).read_text()
    page_path = root / (sys.argv[2] if len(sys.argv) > 2 else "index.html")
    page = page_path.read_text()

    if "</script>" in scad:
        sys.exit("refusing to embed: the model contains a closing script tag")

    new, n = BLOCK.subn(lambda m: m.group(1) + scad + m.group(2), page, count=1)
    if not n:
        sys.exit('no <script id="scad-source"> block found in the page')

    if new != page:
        page_path.write_text(new)
        print(f"embedded {len(scad)} bytes of OpenSCAD into {page_path.name}")
    else:
        print("already up to date")


if __name__ == "__main__":
    main()
