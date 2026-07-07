from pathlib import Path
from .rom import ROMImage


class ROMSet:
    def __init__(self, roms):
        if len(roms) != 4:
            raise ValueError("ROMSet requires exactly four ROMs")

        self.roms = roms

        sizes = {len(r) for r in roms}
        if len(sizes) != 1:
            raise ValueError("All ROMs must have identical size")

        self.size = roms[0].size

    @classmethod
    def from_files(cls, files):
        return cls([ROMImage(f) for f in files])

    def names(self):
        return [r.name for r in self.roms]

    def linear(self):
        return b"".join(r.data for r in self.roms)

    def interleave8(self):
        out = bytearray()

        for i in range(self.size):
            for r in self.roms:
                out.append(r.data[i])

        return bytes(out)

    def interleave16be(self):
        out = bytearray()

        for i in range(0, self.size, 2):
            for r in self.roms:
                out.extend(r.data[i:i + 2])

        return bytes(out)

    def interleave32be(self):
        out = bytearray()

        for i in range(0, self.size, 4):
            for r in self.roms:
                out.extend(r.data[i:i + 4])

        return bytes(out)

    def builds(self):
        return {
            "linear": self.linear(),
            "interleave8": self.interleave8(),
            "interleave16": self.interleave16be(),
            "interleave32": self.interleave32be(),
        }

    def save_builds(self, outdir):
        outdir = Path(outdir)
        outdir.mkdir(parents=True, exist_ok=True)

        written = []

        for name, data in self.builds().items():
            filename = outdir / f"{name}.bin"

            with open(filename, "wb") as f:
                f.write(data)

            written.append(filename)

        return written