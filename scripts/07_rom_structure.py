#!/usr/bin/env python3
"""
07_rom_structure.py

Build a high-level structural map of the reconstructed ROM.
"""

from pathlib import Path
from collections import Counter
import math

ROM = Path("output/builds/interleave16.bin")

WINDOW = 4096

data = ROM.read_bytes()

print("=" * 72)
print(" Triton ROM Structure Analyzer")
print("=" * 72)
print()

print(f"ROM size : {len(data):,} bytes")
print(f"Window   : {WINDOW} bytes")
print()

print("Offset       Entropy")
print("---------------------------")

for offset in range(0, len(data), WINDOW):

    block = data[offset:offset + WINDOW]

    counts = Counter(block)

    entropy = 0.0

    for n in counts.values():
        p = n / len(block)
        entropy -= p * math.log2(p)

    print(f"{offset:08X}    {entropy:5.2f}")