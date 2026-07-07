# Korg Triton Rack Reverse Engineering

## Current status

The repository contains:

- original ROM dumps
- donor ROM dumps
- ROM comparison tools
- ROM builder
- automatic build analyzer

---

# Hardware

Main board contains:

- 4 × MBM29F160BE Flash
- Hitachi SH7034 CPU
- Two custom KORG DSPs
- Boot failure:
    System Error
    Code 9

---

# Confirmed observations

## ROM size

Each ROM:

2097152 bytes

Combined image:

8388608 bytes

---

## Tested build methods

- Linear
- Interleave 8-bit
- Interleave 16-bit
- Interleave 32-bit

All produce valid 8 MB images.

---

## Entropy

All four combined images:

5.7344

This is expected because only ordering changes.

---

## Linear build

Longest FF run:

93264 bytes

Longest 00 run:

331420 bytes

Conclusion:

Very unlikely to represent real memory layout.

---

## Interleave16

Longest FF:

4 bytes

Longest 00:

86 bytes

Looks much more realistic.

---

## Interleave32

Longest FF:

6 bytes

Longest 00:

92 bytes

Also looks realistic.

Further investigation required.

---

# Donor ROMs

Donor ROM filenames correspond to PCB silkscreen:

IC3
IC12
IC17
IC23

This appears intentional.

---

# User ROMs

Files:

1x1
1x2
1x3
1x4

2x1
2x2
2x3
2x4

Known fact:

1x2 == 2x2

Reason:

ROMs were rewritten using another Triton Rack during OS update.

Therefore this equality is expected.

---

# Current hypothesis

The correct memory mapping is more likely to be:

Interleave16

or

Interleave32

than linear concatenation.

---

# Next step

Search inside generated images for:

- vector tables
- pointer tables
- reset vector
- boot loader
- checksum verification
- ROM identification tables
