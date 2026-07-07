# Korg Triton Rack Reverse Engineering

## Current Goal

Determine why the Triton Rack stops during boot with:

System Error
Code 9

---

# Stage 1 — Infrastructure

Status: ✅ Completed

- [x] GitHub repository created
- [x] ROM comparison tools
- [x] ROM framework
- [x] ROMSet class
- [x] Build generator
- [x] Build analyzer

---

# Stage 2 — Memory Reconstruction

Status: 🟡 In Progress

- [x] Build Linear image
- [x] Build Interleave8 image
- [x] Build Interleave16 image
- [x] Build Interleave32 image

Next:

- [ ] Detect pointer tables
- [ ] Detect vector tables
- [ ] Detect jump tables
- [ ] Detect reset vector
- [ ] Detect interrupt vectors

---

# Stage 3 — CPU Detection

Status: 🔲 Planned

- [ ] Identify executable regions
- [ ] Detect instruction alignment
- [ ] Confirm SH architecture
- [ ] Locate boot loader

---

# Stage 4 — Boot Analysis

Status: 🔲 Planned

- [ ] Reverse startup sequence
- [ ] Locate ROM verification
- [ ] Locate checksum verification
- [ ] Locate board identification
- [ ] Locate hardware initialization

---

# Stage 5 — Error Code 9

Status: 🔲 Planned

- [ ] Locate error table
- [ ] Locate "System Error"
- [ ] Locate Code 9 generation
- [ ] Determine exact failing condition

---

# Stage 6 — Repair

Status: 🔲 Planned

Possible outcomes:

- rebuild ROM
- repair checksum
- repair boot block
- identify defective ROM
- identify hardware dependency