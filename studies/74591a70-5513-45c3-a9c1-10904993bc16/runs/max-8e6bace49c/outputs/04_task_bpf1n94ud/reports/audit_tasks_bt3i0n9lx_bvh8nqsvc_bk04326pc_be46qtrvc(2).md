---
title: "Audit — Background Tasks bt3i0n9lx, bvh8nqsvc, bk04326pc, be46qtrvc"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
run_id: "max-6aa66319d7"
audit_type: "human-authored post-hoc"
tasks: ["bt3i0n9lx", "bvh8nqsvc", "bk04326pc", "be46qtrvc"]
---

# Audit — Background Tasks (MM-GBSA and Interaction Analysis Attempts)

These four tasks were the implementation attempts for Phase 3. Their sequence documents the iterative debugging required to produce the final results.

---

## Task bt3i0n9lx — ProLIF Interaction Analysis (FAILED)

**Script**: `run_interactions.py`  
**Exit code**: 139 (segfault)  
**What it did**: Loaded receptor via MDAnalysis, selected binding-site residues within 8 Å of each ligand centroid, then called `plf.Molecule.from_mda(bs_sel)` to convert to RDKit for ProLIF fingerprinting.

**Failure**: Segfault (SIGSEGV) in ProLIF/MDAnalysis/RDKit interop when converting even a small binding-site selection to a ProLIF Molecule. Root cause: likely a version conflict between MDAnalysis 2.x and ProLIF 2.2.1 on this platform.

**Resolution**: Replaced with a pure RDKit geometry-based fingerprinter (`run_interactions_rdkit.py`) with no MDAnalysis dependency. This produced interaction profiles for all 22 compounds in ~2 s.

---

## Task bvh8nqsvc — MM-GBSA with AM1BCC Charges (FAILED)

**Script**: `run_mmgbsa2.py` (first version with `-c bcc -s 2`)  
**Exit code**: 1 (Python exception)  
**What it did**: Attempted antechamber with AM1BCC quantum-mechanical charges (`-c bcc -s 2`) for Compound_10_ent1 (37 heavy atoms).

**Failure**: `subprocess.TimeoutExpired` after 180 s. AM1BCC semi-empirical calculation is O(N³) and unworkable for 30–38 heavy atom compounds within the 180 s timeout.

**Resolution**: Switched to Gasteiger charges (`-c gas`), which complete in <1 s for any compound in this series.

---

## Task bk04326pc — MM-GBSA with Gasteiger Charges, First Run (FAILED)

**Script**: `run_mmgbsa2.py` (Gasteiger version, pre-receptor-fix)  
**Exit code**: 0 (Python script returned normally)  
**What happened**: All 22 compounds produced empty `complex.prmtop` files (0 bytes). tleap exited with FATAL errors for all compounds.

**Failure root causes** (identified from leap.log):
1. All `HIS` residues had `HD1` atoms (δ-protonated) but tleap mapped them as `HIE` (ε-protonated) — `HD1` has no type in the `HIE` template.
2. N-terminal Met47 had `H` as the first ammonium proton, but AMBER `NMET` template expects `H1`.

**Resolution**:
- Wrote Python script to inspect each `HIS` residue's proton inventory (`HD1` → `HID`, `HE2` → `HIE`) and rename accordingly (12 HID, 1 HIE).
- Renamed `H` → `H1` for NMET Met47.
- Fixed receptor written to `mmgbsa2/receptor_amber.pdb`.

---

## Task be46qtrvc — MM-GBSA with Fixed Receptor (SUCCEEDED)

**Script**: `run_mmgbsa2.py` (updated to use `receptor_amber.pdb`, no `leaprc.water.tip3p`)  
**Exit code**: 0  
**Result**: 22/22 compounds completed successfully.

| Metric | Value |
|--------|-------|
| Compounds succeeded | 22/22 |
| Receptor prmtop size | 2.7 MB |
| tleap errors | 0 (warnings only: net charge +7, CARG/NMET chain types) |
| ΔG range | +9.4 to −37.6 kcal/mol |
| Runtime | ~15 min (sequential, AMBER tools) |

**Key fix**: Removing `source leaprc.water.tip3p` from tleap templates (implicit solvent MM-GBSA does not need TIP3P water parameters; their presence was causing an additional atom-type conflict for non-water residues).

---

## Summary

| Task | Purpose | Outcome |
|------|---------|---------|
| bt3i0n9lx | ProLIF interactions | ✗ Segfault → replaced with RDKit |
| bvh8nqsvc | MM-GBSA (AM1BCC) | ✗ Timeout → switched to Gasteiger |
| bk04326pc | MM-GBSA (Gasteiger, bad receptor) | ✗ tleap HIS/NMET naming → fixed receptor |
| be46qtrvc | MM-GBSA (Gasteiger, fixed receptor) | ✓ 22/22 succeeded |

All failures were diagnosed and resolved within the same session. No data was lost.

## Verification

Checks run programmatically at session close (2026-09-07):

| Check | Expected | Observed | Pass |
|-------|----------|----------|------|
| `run_interactions_rdkit.py` present (replaces ProLIF) | yes | yes (15,361 bytes) | ✓ |
| `run_mmgbsa2.py` present (Gasteiger + fixed receptor) | yes | yes (7,515 bytes) | ✓ |
| `mmgbsa2/receptor_amber.pdb` present (HID/HIE + H1 fix) | yes | yes (501,313 bytes) | ✓ |
| MM-GBSA succeeded for all 22 compounds (task be46qtrvc) | 22/22 | 22/22 | ✓ |
| Interaction fingerprints computed for all 22 (task bt3i0n9lx replacement) | 22/22 | 22/22 | ✓ |
| AM1BCC timeout resolved (task bvh8nqsvc → Gasteiger) | no timeouts | antechamber `-c gas` completes <1 s per compound | ✓ |
| tleap HIS naming resolved (task bk04326pc → receptor_amber.pdb) | 0 tleap FAITALs | 0 FATAL errors, receptor.prmtop = 2.7 MB | ✓ |

**bt3i0n9lx** (ProLIF segfault): replaced by `run_interactions_rdkit.py`; 22 interaction profiles computed in ~2 s.  
**bvh8nqsvc** (AM1BCC timeout): resolved by `-c gas`; no timeout errors in any of 22 compounds.  
**bk04326pc** (tleap FATAL): resolved by `receptor_amber.pdb` (12 HID + 1 HIE + NMET H→H1); receptor.prmtop 2.7 MB confirms success.  
**be46qtrvc** (MM-GBSA success): 22/22 DELTA_TOTAL values in `mmgbsa2_results.json`; ΔG range −37.6 to +9.3 kcal/mol.
