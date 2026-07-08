from pathlib import Path
import sys
import string
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from triton.rom import ROMImage


BUILD_DIR = ROOT / "output" / "builds"


def ascii_strings(data, min_len=4):
    chars = []
    count = 0

    for b in data:
        if 32 <= b <= 126:
            chars.append(chr(b))
        else:
            if len(chars) >= min_len:
                count += 1
            chars = []

    if len(chars) >= min_len:
        count += 1

    return count


def longest_run(data, value):
    best = 0
    cur = 0

    for b in data:
        if b == value:
            cur += 1
            if cur > best:
                best = cur
        else:
            cur = 0

    return best


def repeated_dwords(data):

    c = Counter()

    for i in range(0, len(data) - 4, 4):
        c[data[i:i + 4]] += 1

    repeated = sum(v for v in c.values() if v > 1)

    return repeated


print()

print("=" * 72)
print(" Triton Build Analysis")
print("=" * 72)

for file in sorted(BUILD_DIR.glob("*.bin")):

    rom = ROMImage(file)

    strings = ascii_strings(rom.data)

    ff = longest_run(rom.data, 0xFF)

    zz = longest_run(rom.data, 0x00)

    rep = repeated_dwords(rom.data)

    print()
    print(file.name)
    print("-" * len(file.name))

    print(f"Size             : {rom.size:,}")
    print(f"CRC32            : {rom.crc32()}")
    print(f"Entropy          : {rom.entropy():.4f}")

    print(f"ASCII strings    : {strings}")

    print(f"Longest FF run   : {ff}")

    print(f"Longest 00 run   : {zz}")

    print(f"Repeated DWORDs  : {rep}")