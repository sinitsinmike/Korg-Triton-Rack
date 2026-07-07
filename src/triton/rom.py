from __future__ import annotations

from pathlib import Path
import hashlib
import zlib
import math
from collections import Counter


class ROMImage:
    def __init__(self, filename):
        self.path = Path(filename)
        self.name = self.path.name
        self.data = self.path.read_bytes()
        self.size = len(self.data)

    def __len__(self):
        return self.size

    def read8(self, addr):
        return self.data[addr]

    def read16be(self, addr):
        return int.from_bytes(self.data[addr:addr + 2], "big")

    def read16le(self, addr):
        return int.from_bytes(self.data[addr:addr + 2], "little")

    def read32be(self, addr):
        return int.from_bytes(self.data[addr:addr + 4], "big")

    def read32le(self, addr):
        return int.from_bytes(self.data[addr:addr + 4], "little")

    def slice(self, start, end):
        return self.data[start:end]

    def sha1(self):
        return hashlib.sha1(self.data).hexdigest()

    def md5(self):
        return hashlib.md5(self.data).hexdigest()

    def crc32(self):
        return "%08X" % (zlib.crc32(self.data) & 0xffffffff)

    def entropy(self):
        counts = Counter(self.data)

        e = 0.0

        for c in counts.values():
            p = c / self.size
            e -= p * math.log2(p)

        return e

    def find(self, pattern):

        if isinstance(pattern, str):
            pattern = pattern.encode()

        pos = 0

        while True:

            p = self.data.find(pattern, pos)

            if p == -1:
                break

            yield p

            pos = p + 1

    def hexdump(self, start=0, length=256):

        end = min(start + length, self.size)

        for off in range(start, end, 16):

            chunk = self.data[off:off + 16]

            hexs = " ".join(f"{b:02X}" for b in chunk)

            asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)

            print(f"{off:08X}  {hexs:<47} {asc}")

    def info(self):

        print()

        print(self.name)

        print("-" * len(self.name))

        print(f"Size     : {self.size:,}")
        print(f"CRC32    : {self.crc32()}")
        print(f"MD5      : {self.md5()}")
        print(f"SHA1     : {self.sha1()}")
        print(f"Entropy  : {self.entropy():.4f}")

        print()