from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from triton.romset import ROMSet
from triton.rom import ROMImage

rom_dir = ROOT / "roms"

files = [
    rom_dir / "IC23 (992742) MBM29F160BE chksum 617885D.bin",
    rom_dir / "IC17 (992642) MBM29F160BE chksum A0B614C.bin",
    rom_dir / "IC12 (992542) MBM29F160BE chksum 626A09F.bin",
    rom_dir / "IC3 (992442) MBM29F160BE chksum B4F098D.bin",
]

rs = ROMSet.from_files(files)

outdir = ROOT / "output" / "builds"

written = rs.save_builds(outdir)

print()

print("Generated images")

print("----------------")

for f in written:

    rom = ROMImage(f)

    print(f.name)

    print(" Size    :", rom.size)
    print(" CRC32   :", rom.crc32())
    print(" Entropy :", round(rom.entropy(),4))

    print()