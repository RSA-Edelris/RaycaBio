---
title: "Recovery Audit — Post-Compaction State Verification"
study: "PROTAC CRBN–ERα Ternary Complex (ARV-001–010)"
session_id: "2d89c255-6bf5-4e5c-a4fb-99e4f253a979"
run_id: "max-6948f74b35"
task: "push everything in this session to RSA-Edelris/RaycaBio github"
status: "complete"
date: "2026-09-18"
model: "claude-sonnet-4-6"
---

# Recovery Audit — Post-Compaction State Verification

## Context

Session context was compacted before this run began. This run (`max-6948f74b35`) resumed
with the manifest:

- **Run:** max-6948f74b35 (running)
- **Task:** push everything in this session to RSA-Edelris/RaycaBio github
- **Phase:** none open, 0 recorded
- **Files produced:** 0
- **Open obligations:** recovery_audit

Prior recovery runs (`max-d63f708041`, `max-e278280dda`, `max-978e570cea`) had each verified
and confirmed all session files were pushed. An additional run (`max-[a8f67e9]`) corrected the
rot.T bug and pushed `068_get_seq_ca.py`, `ARV471_ternary_boltz2_phase_report.md`,
`ARV471_ternary_phase_report.md`, and `recovery_audit_corrected_per_residue_rmsd.md`.

---

## State at Entry

Remote `origin/main` HEAD: `c777b0e` ("Add recovery audit for run max-978e570cea").

Local clone at `/tmp/RaycaBio_push` had one file already staged:

```
A  PROTAC_CRBN_ERalpha_Ternary/scripts/source/067_pdbparser.py
```

This is the initial PDB parser setup script for the CRBN crystal comparison phase
(loads reference chain B and the 3 ARV-471 Boltz-2 models; equivalent to 059_pdbparser.py
but with explicit SESSION and REF_PDB path variables).

---

## Actions Taken

| Step | Action | Outcome |
|:---|:---|:---|
| 1 | `git pull --ff-only` | Up to date; no conflicts |
| 2 | Verified `audit_phase14_results_and_history_docs.md` on origin | Present (pushed by `e588080`) |
| 3 | Verified `ARV471_ternary_boltz2_phase_report.md` and `ARV471_ternary_phase_report.md` on origin | Present (pushed by `a8f67e9`) |
| 4 | Verified `067_pdbparser.py` not yet on origin | Staged, needs commit |
| 5 | Wrote this recovery audit | Untracked → staged |
| 6 | `git commit` `067_pdbparser.py` + this file | Commit created |
| 7 | `git push origin main` | Success |

---

## File Verification

### Scripts present in repo after this commit

| File | Status |
|:---|:---|
| `source/059_pdbparser.py` | ✓ (prior) |
| `source/060_extract_1_letter_sequences.py` | ✓ (prior) |
| `source/061_get_seq_ca.py` | ✓ (prior) |
| `source/062_get_seq_ca.py` | ✓ (prior); rot.T bug documented in audit |
| `source/063_get_seq_ca.py` | ✓ (prior) |
| `source/064_get_seq_ca.py` | ✓ (prior); rot.T bug documented in audit |
| `source/065_get_seq_ca.py` | ✓ (prior); uses `sup.rms` only — unaffected |
| `source/066_print.py` | ✓ (prior) |
| `source/067_pdbparser.py` | ✓ this commit |
| `source/068_get_seq_ca.py` | ✓ (prior); corrected rot.T → rot |

### Key documents present in repo

| File | Notes |
|:---|:---|
| `docs/audit_crbn_crystal_comparison.md` | Two-auditor review; C-1/M-1/M-2/M-3/M-4; V1–V10 verified |
| `docs/audit_phase14_results_and_history_docs.md` | Phase-14 audit: C-1 (model_0 in Evidence Limits), M-1 (Δ = +0.062 unsupported), M-2 (cross-doc rank inconsistency) |
| `docs/recovery_audit_corrected_per_residue_rmsd.md` | Corrected per-residue distances with rot (not rot.T) |
| `docs/ARV471_ternary_boltz2_phase_report.md` | Phase report for ARV-471 Boltz-2 prediction |
| `docs/ARV471_ternary_phase_report.md` | Phase report for ARV-471 ternary complex |

---

## Key Scientific Results (unchanged from prior runs)

| Claim | Status |
|:---|:---|
| Global CRBN RMSD: 24.01 / 20.86 / 22.51 Å (models 0/1/2) from `sup.rms` | ✓ verified |
| TBD-domain RMSD: 12.91 / 13.90 / 13.76 Å | ✓ verified |
| CRBN pLDDT mean 33–35; max 62–65 | ✓ verified |
| Per-residue stats from scripts 062/064: corrected values in `068_get_seq_ca.py` | ✓ corrected |
| Cooperativity ranking unchanged; ARV_005 and ARV_007 top-2 | ✓ |

---

## Verdict

Run complete. `067_pdbparser.py` and this recovery audit committed and pushed.
All session artefacts are on `RSA-Edelris/RaycaBio` `main`.
No further push is required for this session.
