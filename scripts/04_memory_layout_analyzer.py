#!/usr/bin/env python3

from pathlib import Path
from collections import Counter
import math
import zlib

BUILD_DIR = Path("output/builds")


def entropy(data):
    counts = Counter(data)
    total = len(data)
    e = 0.0
    for c in counts.values():
        p = c / total
        e -= p * math.log2(p)
    return e


def longest_run(data, value):
    longest = 0
    current = 0

    for b in data:
        if b == value:
            current += 1
            longest = max(longest, current)
        else:
            current = 0

    return longest


def ascii_strings(data, min_len=4):
    count = 0
    current = 0

    for b in data:
        if 32 <= b <= 126:
            current += 1
        else:
            if current >= min_len:
                count += 1
            current = 0

    if current >= min_len:
        count += 1

    return count


def repeated_blocks(data, block=16):
    seen = {}

    for i in range(0, len(data) - block, block):
        b = data[i:i + block]
        seen[b] = seen.get(b, 0) + 1

    repeated = sum(1 for v in seen.values() if v > 1)
    return repeated


def score(ent, ff, zz, strings, repeats):
    s = 100.0

    if ent < 5.0:
        s -= 20

    if ff > 10000:
        s -= 20

    if zz > 10000:
        s -= 20

    s += min(strings / 2000.0, 15)

    s += min(repeats / 5000.0, 10)

    return round(s, 2)


def analyze(path):

    data = path.read_bytes()

    ent = entropy(data)
    ff = longest_run(data, 0xFF)
    zz = longest_run(data, 0x00)
    strings = ascii_strings(data)
    repeats = repeated_blocks(data)

    crc = zlib.crc32(data) & 0xffffffff

    sc = score(ent, ff, zz, strings, repeats)

    return {
        "name": path.name,
        "size": len(data),
        "entropy": ent,
        "crc": crc,
        "ff": ff,
        "zz": zz,
        "strings": strings,
        "repeats": repeats,
        "score": sc,
    }


def main():

    builds = sorted(BUILD_DIR.glob("*.bin"))

    if not builds:
        print("No builds found.")
        return

    results = []

    print()
    print("=" * 72)
    print(" Triton Memory Layout Analyzer")
    print("=" * 72)

    for b in builds:

        r = analyze(b)
        results.append(r)

        print()
        print(r["name"])
        print("-" * len(r["name"]))

        print(f'Size              : {r["size"]:,}')
        print(f'CRC32             : {r["crc"]:08X}')
        print(f'Entropy           : {r["entropy"]:.4f}')
        print(f'ASCII strings     : {r["strings"]}')
        print(f'Longest FF run    : {r["ff"]}')
        print(f'Longest 00 run    : {r["zz"]}')
        print(f'Repeated blocks   : {r["repeats"]}')
        print(f'Score             : {r["score"]:.2f}')

    print()
    print("=" * 72)
    print(" Candidate Ranking")
    print("=" * 72)

    results.sort(key=lambda x: x["score"], reverse=True)

    for i, r in enumerate(results, 1):
        print(f'{i}. {r["name"]:<20} {r["score"]:6.2f}')

    print()


if __name__ == "__main__":
    main()