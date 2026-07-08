# Korg Triton Rack Reverse Engineering

**Project Status:** Phase 2 — Reverse Engineering

Last Updated: 2026-07-08

---

# Objective

Determine the complete boot process of the Korg Triton Rack firmware and identify the exact reason for:

System Error
Code 9

---

# Confirmed Facts

## F-001 — Flash ROM Size

Status: 🟢 Confirmed

Each Fujitsu MBM29F160BE contains:

- 2,097,152 bytes (2 MB)

---

## F-002 — Total Flash Size

Status: 🟢 Confirmed

The main board contains four Flash devices.

Total firmware size:

8,388,608 bytes (8 MB)

---

## F-003 — Donor ROM Naming

Status: 🟢 Confirmed

The donor ROM filenames correspond to the PCB silkscreen:

- IC3
- IC12
- IC17
- IC23

---

## F-004 — Updated ROM Equality

Status: 🟢 Confirmed

ROM:

1x2

is identical to

2x2

Reason:

Both chips were rewritten using another working Triton Rack during an official firmware update.

This behavior is expected.

---

# Experiments

## E-001 — ROM Comparison

Status: 🟢 Completed

Result:

ROM comparison tools successfully identify identical and different Flash devices.

---

## E-002 — ROM Reconstruction

Status: 🟢 Completed

Generated images:

- Linear
- Interleave 8-bit
- Interleave 16-bit
- Interleave 32-bit

Each image size:

8 MB

---

## E-003 — Build Analysis

Status: 🟢 Completed

Results:

All reconstructed images have identical entropy.

Entropy:

5.7344

Linear image contains extremely large FF and 00 regions.

Interleave16 and Interleave32 contain much shorter FF/00 regions.

---

# Hypotheses

## H-001

Linear concatenation represents the real memory layout.

Status:

🔴 Rejected (current evidence)

Reason:

Very large contiguous FF and 00 regions.

---

## H-002

Interleave16 represents the real memory layout.

Status:

🟡 Under Investigation

---

## H-003

Interleave32 represents the real memory layout.

Status:

🟡 Under Investigation

---

## H-004

System Error Code 9 is generated after ROM integrity verification.

Status:

🔵 Open

---

# Next Tasks

- Pointer analysis
- Vector table detection
- CPU code detection
- Memory map reconstruction
- Boot sequence reconstruction
- Error Code 9 localization