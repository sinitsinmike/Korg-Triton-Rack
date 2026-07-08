#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.insert(0, "src")

from triton.pointer import PointerScanner


BUILD_DIR = Path("output/builds")


def main():

    for image in sorted(BUILD_DIR.glob("*.bin")):

        scanner = PointerScanner(image)
        scanner.report()


if __name__ == "__main__":
    main()