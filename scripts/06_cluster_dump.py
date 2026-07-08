#!/usr/bin/env python3

from pathlib import Path
import struct
import sys

sys.path.insert(0, "src")

from triton.pointer import PointerScanner

BUILD = Path("output/builds/interleave16.bin")


def hexdump(data, start, length=64):

    end = min(start + length, len(data))

    for off in range(start, end, 16):

        chunk = data[off:off + 16]

        hexpart = " ".join(f"{b:02X}" for b in chunk)

        asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)

        print(f"{off:08X}  {hexpart:<47}  {asc}")


def main():

    scanner = PointerScanner(BUILD)

    pointers = scanner.scan32()

    clusters = scanner.clusters(pointers)

    print()
    print("=" * 72)
    print(BUILD.name)
    print("=" * 72)
    print()

    print(f"Clusters found: {len(clusters)}")
    print()

    while True:

        try:
            n = input("Cluster number (q=quit): ")

            if n.lower() == "q":
                break

            idx = int(n) - 1

            cluster = clusters[idx]

        except Exception:
            print("Invalid cluster.")
            continue

        print()
        print("=" * 72)
        print(f"Cluster {idx+1}")
        print("=" * 72)

        print()

        print(f"Offset : 0x{cluster[0][0]:08X}")
        print(f"Length : {len(cluster)}")
        print()

        print("Pointers")
        print("--------")

        for i, (_, value) in enumerate(cluster):

            print(f"{i:2d}: 0x{value:08X}")

        print()

        print("HEX around cluster")
        print("------------------")

        hexdump(scanner.data, cluster[0][0], 128)

        print()

        print("Targets")
        print("-------")

        shown = 0

        for _, value in cluster:

            if value >= len(scanner.data):
                continue

            print()
            print(f"Target 0x{value:08X}")

            hexdump(scanner.data, value, 32)

            shown += 1

            if shown >= 5:
                break

        print()


if __name__ == "__main__":
    main()