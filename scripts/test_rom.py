from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from triton.rom import ROMImage

rom_dir = ROOT / "roms"

files = sorted(
    list(rom_dir.glob("*.bin")) +
    list(rom_dir.glob("*.BIN"))
)

if not files:
    raise RuntimeError("No ROM files found")

print("Available ROMs:")

for i, f in enumerate(files):
    print(f"{i}: {f.name}")

print()

rom = ROMImage(files[0])

rom.info()

print("First 64 bytes\n")

rom.hexdump(0, 64)