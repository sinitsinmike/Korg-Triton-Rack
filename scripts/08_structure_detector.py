#!/usr/bin/env python3
"""
08_structure_detector.py

Search for repeating fixed-size records in the ROM.
"""

from pathlib import Path
from collections import Counter

ROM = Path("output/builds/interleave16.bin")

START = 0x003A9000
END   = 0x00420000

data = ROM.read_bytes()

sizes = [16, 24, 32, 64]

print("=" * 72)
print(" Triton Structure Detector")
print("=" * 72)

print()

for size in sizes:

    print(f"Record size {size} bytes")
    print("-" * 32)

    records = []

    for off in range(START, END, size):

        records.append(data[off:off+size])

    unique = len(set(records))

    print(f"Records : {len(records)}")
    print(f"Unique  : {unique}")

    if unique != len(records):
        print("Repeated structures detected")

    print()