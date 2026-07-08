from pathlib import Path
import struct


class PointerScanner:
    """
    Scan a ROM image for possible pointer tables.

    The scanner itself does not assume any CPU architecture.
    It simply looks for values that appear to point somewhere
    inside the current image.
    """

    def __init__(self, filename):

        self.path = Path(filename)
        self.data = self.path.read_bytes()
        self.size = len(self.data)

    def scan32(self):

        pointers = []

        for offset in range(0, self.size - 4, 4):

            value = struct.unpack_from("<I", self.data, offset)[0]

            if value < self.size:
                pointers.append((offset, value))

        return pointers

    def clusters(self, pointers, gap=4, minimum=8):

        clusters = []

        if not pointers:
            return clusters

        current = [pointers[0]]

        for p in pointers[1:]:

            if p[0] - current[-1][0] == gap:
                current.append(p)
            else:
                if len(current) >= minimum:
                    clusters.append(current)
                current = [p]

        if len(current) >= minimum:
            clusters.append(current)

        return clusters

    def report(self):

        pointers = self.scan32()
        clusters = self.clusters(pointers)

        print()
        print("=" * 72)
        print(self.path.name)
        print("=" * 72)

        print(f"Possible pointers : {len(pointers)}")
        print(f"Pointer clusters  : {len(clusters)}")
        print()

        for i, cluster in enumerate(clusters[:20], 1):

            print(
                f"{i:2d}. "
                f"Offset 0x{cluster[0][0]:08X}   "
                f"Length {len(cluster)}"
            )