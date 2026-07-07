#!/usr/bin/env python3

import hashlib
import zlib
import math
from pathlib import Path
from collections import Counter
import json

ROM_DIR = Path("roms")
OUT_DIR = Path("output")

OUT_DIR.mkdir(exist_ok=True)

def entropy(data):
    if not data:
        return 0.0

    counts = Counter(data)
    total = len(data)

    ent = 0.0

    for c in counts.values():
        p = c / total
        ent -= p * math.log2(p)

    return ent

report = []
md = []

print()
print("Scanning ROMs...")
print()

roms = sorted([f for f in ROM_DIR.iterdir() if f.suffix.lower() == ".bin"])

for rom in roms:

    data = rom.read_bytes()

    crc = "%08X" % (zlib.crc32(data) & 0xffffffff)

    md5 = hashlib.md5(data).hexdigest()

    sha1 = hashlib.sha1(data).hexdigest()

    ent = entropy(data)

    first = data[:16].hex(" ")

    last = data[-16:].hex(" ")

    ascii_count = sum(32 <= b <= 126 for b in data)

    utf16_pairs = 0

    for i in range(0, len(data)-1, 2):
        if data[i+1] == 0 and 32 <= data[i] <= 126:
            utf16_pairs += 1

    ascii_percent = ascii_count / len(data) * 100
    utf16_percent = utf16_pairs / (len(data)/2) * 100

    item = {
        "file": rom.name,
        "size": len(data),
        "crc32": crc,
        "md5": md5,
        "sha1": sha1,
        "entropy": round(ent,4),
        "ascii_percent": round(ascii_percent,2),
        "utf16_percent": round(utf16_percent,2),
        "first16": first,
        "last16": last,
    }

    report.append(item)

    md.append(f"# {rom.name}")
    md.append("")
    md.append(f"* Size: {len(data):,}")
    md.append(f"* CRC32: `{crc}`")
    md.append(f"* MD5: `{md5}`")
    md.append(f"* SHA1: `{sha1}`")
    md.append(f"* Entropy: **{ent:.4f}**")
    md.append(f"* ASCII: {ascii_percent:.2f}%")
    md.append(f"* UTF16-like: {utf16_percent:.2f}%")
    md.append("")
    md.append(f"First16:")
    md.append("```")
    md.append(first)
    md.append("```")
    md.append("")
    md.append(f"Last16:")
    md.append("```")
    md.append(last)
    md.append("```")
    md.append("")

with open(OUT_DIR/"report.json","w") as f:
    json.dump(report,f,indent=4)

with open(OUT_DIR/"report.md","w") as f:
    f.write("\n".join(md))

print("Done.")
print()
print("Report saved to:")
print("output/report.md")
print("output/report.json")
print()