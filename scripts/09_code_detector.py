#!/usr/bin/env python3

"""
09_code_detector.py

Search for ROM regions that are likely to contain executable code.
"""

from pathlib import Path
from collections import Counter
import math

ROM = Path("output/builds/interleave16.bin")

WINDOW = 4096

data = ROM.read_bytes()

print("=" * 72)
print(" Triton Code Detector")
print("=" * 72)
print()

results = []

for offset in range(0, len(data), WINDOW):

    block = data[offset:offset + WINDOW]

    counts = Counter(block)

    entropy = 0.0

    for n in counts.values():
        p = n / len(block)
        entropy -= p * math.log2(p)

    # candidate executable code usually has medium entropy
    if 5.5 <= entropy <= 7.2:
        results.append((offset, entropy))

print(f"Candidate regions: {len(results)}")
print()

for offset, entropy in results[:100]:
    print(f"{offset:08X}    entropy {entropy:.2f}")