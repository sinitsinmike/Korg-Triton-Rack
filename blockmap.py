#!/usr/bin/env python3

from pathlib import Path
from itertools import combinations
import hashlib

ROM_DIR = Path("roms")
OUT_DIR = Path("output")
OUT_DIR.mkdir(exist_ok=True)

BLOCK = 4096          # 4 KB

roms = sorted(ROM_DIR.glob("*.bin")) + sorted(ROM_DIR.glob("*.BIN"))

images = {}

for f in roms:
    images[f.name] = f.read_bytes()

report = []

for a, b in combinations(images.keys(), 2):

    d1 = images[a]
    d2 = images[b]

    size = min(len(d1), len(d2))

    blocks = size // BLOCK

    report.append("=" * 80)
    report.append(f"{a}")
    report.append(f"{b}")
    report.append("")

    equal = 0

    for i in range(blocks):

        off = i * BLOCK

        h1 = hashlib.md5(d1[off:off+BLOCK]).digest()
        h2 = hashlib.md5(d2[off:off+BLOCK]).digest()

        if h1 == h2:
            equal += 1

    report.append(f"Equal blocks : {equal}/{blocks}")
    report.append("")

    line = ""

    for i in range(blocks):

        off = i * BLOCK

        h1 = hashlib.md5(d1[off:off+BLOCK]).digest()
        h2 = hashlib.md5(d2[off:off+BLOCK]).digest()

        line += "█" if h1 == h2 else "·"

        if len(line) == 64:
            report.append(line)
            line = ""

    if line:
        report.append(line)

    report.append("")

(Path("output") / "blockmap.txt").write_text("\n".join(report))

print("Saved output/blockmap.txt")