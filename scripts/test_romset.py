from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from triton.romset import ROMSet

rom_dir = ROOT / "roms"

donor = [
    rom_dir / "IC23 (992742) MBM29F160BE chksum 617885D.bin",
    rom_dir / "IC17 (992642) MBM29F160BE chksum A0B614C.bin",
    rom_dir / "IC12 (992542) MBM29F160BE chksum 626A09F.bin",
    rom_dir / "IC3 (992442) MBM29F160BE chksum B4F098D.bin",
]

rs = ROMSet.from_files(donor)

print("ROM order:")
for n in rs.names():
    print(" ", n)

print()

print("Linear size      :", len(rs.linear()))
print("Interleave8 size :", len(rs.interleave8()))
print("Interleave16 size:", len(rs.interleave16be()))
print("Interleave32 size:", len(rs.interleave32be()))