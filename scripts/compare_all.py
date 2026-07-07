#!/usr/bin/env python3

from pathlib import Path
from itertools import combinations

ROM_DIR = Path("roms")
OUT_DIR = Path("output")

OUT_DIR.mkdir(exist_ok=True)

roms = sorted([f for f in ROM_DIR.iterdir() if f.suffix.lower()==".bin"])

data = {}

for f in roms:
    data[f.name] = f.read_bytes()

report=[]

for a,b in combinations(data.keys(),2):

    d1=data[a]
    d2=data[b]

    diff=0

    ranges=[]

    start=None

    for i,(x,y) in enumerate(zip(d1,d2)):

        if x!=y:

            diff+=1

            if start is None:
                start=i

        else:

            if start is not None:
                ranges.append((start,i-1))
                start=None

    if start is not None:
        ranges.append((start,len(d1)-1))

    report.append((a,b,diff,ranges))

with open(OUT_DIR/"compare_report.txt","w") as f:

    for a,b,diff,ranges in report:

        f.write("="*70+"\n")
        f.write(f"{a}\n")
        f.write(f"{b}\n")
        f.write(f"Different bytes : {diff}\n")
        f.write(f"Different regions : {len(ranges)}\n")

        for s,e in ranges[:30]:
            f.write(f"  {s:06X}-{e:06X} ({e-s+1})\n")

        if len(ranges)>30:
            f.write("  ...\n")

        f.write("\n")

print()

print("Done.")

print()

print("Saved:")

print("output/compare_report.txt")