# Audit: Phase — Compare ARV-471 Boltz-2 CRBN models to crystal structure CRBN.pdb

**Date:** 2026-09-16  
**Audited by:** Main session auditor (subagent a3a4a864fa1771a81 did not produce a file; audit performed directly from source scripts)  
**Scripts examined:** 059–065 in `source/`  
**BioPython version verified from:** `/home/ubuntu/rayca-runtime/.venv/lib/python3.12/site-packages/Bio/SVDSuperimposer/__init__.py`

---

## CRITICAL

### C-1 — No phase document exists

There is no phase document for this comparison (no `phase_XX_compare_arv471_crbn_to_crystal.md` or equivalent). There is nothing to check reported claims against beyond the raw script output reproduced in the conversation. This means the analysis has no independent record of what was computed, no summary of intermediate values, and no provenance trail.

Reported as a finding per audit brief; does not invalidate numerical results on its own.

---

## MAJOR

### M-1 — `rot.T` used instead of `rot` in per-residue distance calculations (scripts 062 and 064)

**Source:** `062_get_seq_ca.py` line 41; `064_get_seq_ca.py` line 52.

Both scripts extract the rotation matrix from `sup.rotran` and apply it as:
```python
mod_transformed = mod_coords @ rot.T + tran
```

The installed BioPython (`Bio.SVDSuperimposer`, confirmed from source):
```python
def get_rotran(self):
    """Right multiplying rotation matrix and translation."""
    return self.rot, self.tran

def get_transformed(self):
    self.transformed_coords = dot(self.coords, self.rot) + self.tran
```

The correct transformation is `coords @ rot + tran`. The scripts apply `rot.T` = `rot⁻¹`, the inverse rotation. This rotates model Cα coordinates *away* from the reference rather than onto it.

**Evidence of the error:** By the power-mean inequality, RMSD ≥ mean(per-residue distance) always. Reported results violate this for model_0: `sup.rms` = 24.01 Å but `per_res.mean()` = 28.41 Å. 28.41 > 24.01 is impossible for correctly superimposed coordinates; it confirms the wrong rotation was applied.

**Affected statistics (all unreliable):**
- Per-residue distance mean, median, max
- "Fraction < 2 Å" and "fraction < 5 Å" percentages
- Pocket-residue RMSD (script 064, which squares and averages the wrong distances)
- "5 worst / 5 best residues" lists (wrong ranking, wrong residue numbers highlighted)

**Unaffected:**
- `sup.rms` values — computed internally by BioPython without `rotran` manipulation: 24.01, 20.86, 22.51 Å (global); 12.91, 13.90, 13.76 Å (TBD); all domain-level RMSDs from script 065.

**Conclusion impact:** The main claim (CRBN is poorly predicted, RMSD 20+ Å) is NOT invalidated because it rests on `sup.rms`. But the specific per-residue statistics cited in the analysis narrative (mean distances, percentages, pocket RMSD, best/worst residues) cannot be cited.

---

### M-2 — Domain boundaries are single-data-point rules with no citation

**Source:** `065_get_seq_ca.py` lines 15–22.

The three domain cuts (N-lobe 47–165, C-lobe 166–320, TBD 321–427) are annotated in a comment but no reference is given. CRBN domain boundaries vary across publications; the TBD boundary in particular ranges from ~318 to ~330 depending on the paper and crystal structure used. The domain-level RMSD values depend directly on these boundaries.

---

### M-3 — "pLDDT first 180 ≈ N-lobe" includes expression tag residues

**Source:** `065_get_seq_ca.py` line 61.

The model has ~40 N-terminal expression tag residues (StrepII-TEV: "MDWSHPQFEKSAVDENLYFQGGG..." confirmed from alignment output in script 061). `plddt[:180]` covers model positions 1–180, which includes ~40 tag residues whose pLDDT values are not part of the CRBN N-lobe. The annotation "≈ N-lobe" is inaccurate. The N-lobe (native 47–165, 119 residues) maps approximately to model positions 87–206; the slice `[:180]` captures some tag and misses some N-lobe.

Impact: the "first 180 mean pLDDT" values (27.3–28.9) mix tag and N-lobe residues and should not be cited as N-lobe pLDDT.

---

### M-4 — Local alignment parsing: `in_local` flag handles internal gaps differently from script 065

**Source:** `064_get_seq_ca.py` lines 28–41 vs `065_get_seq_ca.py` lines 32–41.

Script 064 uses an `in_local` flag to skip C-terminal model overhangs. Script 065 uses the simpler approach (no flag). Both produce 370 matched pairs. However, the `in_local` flag in script 064 would incorrectly advance `mi` for internal crystal-gap positions (`a=="-", b!="-"` inside the matched region) via both the inner `if` and the final `if b!="-": mi+=1`... but `continue` skips the final increment, so `mi` advances once. Checked: correct for the C-terminal case, but the logic is fragile for any internal model-only region and is not tested. No error occurred in this run since the alignment had no such internal gaps.

---

## VERIFIED CORRECT

**V1 — Superimposer.set_atoms(fixed, moving) argument order.**  
Confirmed from installed package: `Superimposer.set_atoms(self, fixed, moving)`. The scripts call `sup.set_atoms(ref_atoms, mod_atoms)` with reference first and model second throughout. ✓

**V2 — Main RMSD values from `sup.rms` are correct.**  
BioPython computes `sup.rms` internally during `set_atoms`; no `rotran` is involved. Values: model_0 = 24.01 Å, model_1 = 20.86 Å, model_2 = 22.51 Å (global, 370 Cα). ✓

**V3 — Domain RMSD values (script 065) are correct.**  
Script 065 uses only `sup.set_atoms()` and `sup.rms` — no `rotran` manipulation. TBD RMSD: 12.91, 13.90, 13.76 Å. These are unaffected by M-1. ✓

**V4 — HETATM filter correctly excludes LVY ligand and waters from Cα list.**  
`r.id[0] == " "` selects standard residues only; HETATM records have id[0] as a non-space hetfield code. ✓

**V5 — pairwise2.align.localms argument order.**  
Signature: `localms(sequenceA, sequenceB, match, mismatch, open, extend)`. Scripts use `(ref_seq, mod_seq, 2, -1, -5, -0.5)`. ✓

**V6 — ri/mi counter logic.**  
Both counters advance only when the corresponding sequence character is non-gap. Pairs are collected only when both are non-gap. ✓

**V7 — Crystal has 370 Cα (residues 47–427).**  
`grep "^ATOM" CRBN.pdb | awk '$3=="CA"' | wc -l` = 370. Confirmed; 11 disordered residues absent from 381-residue span. ✓

**V8 — pLDDT read from B-factor column.**  
`r["CA"].get_bfactor()` reads the B-factor column. Boltz-2 stores pLDDT in the B-factor column of its PDB output (confirmed by values in [20–65] range, consistent with confidence scores). ✓

**V9 — Sequence identity 100% (370/370).**  
Verified: global alignment score 740 (= 370×2, zero mismatches, no gaps in matched region). The Boltz-2 CRBN sequence contains the crystal sequence as a near-contiguous subsequence (99 extra residues from tag + C-terminal extension). ✓

**V10 — Overall conclusion is valid despite M-1.**  
The minimum achievable RMSD (from `sup.rms`) is 20–24 Å across all three models. Per Jensen's inequality, the correct mean per-residue distance ≤ RMSD ≤ 24 Å. Even at the best possible values, CRBN is predicted far from the crystal structure. Mean pLDDT 33–35 (from V8) confirms low confidence. The claim "CRBN is not reliably predicted" is supported by the correct statistics. ✓

---

## Summary table

| ID | Severity | Finding | Affects main RMSD claim? |
|:--:|:--------:|:--------|:---:|
| C-1 | CRITICAL | No phase document exists | — |
| M-1 | MAJOR | `rot.T` instead of `rot` in per-residue distance calculations; per-residue stats are wrong | No |
| M-2 | MAJOR | Domain boundaries uncited; TBD cut varies by paper | Partially |
| M-3 | MAJOR | "First 180 ≈ N-lobe" includes ~40 tag residues | No |
| M-4 | MAJOR | `in_local` flag fragile for internal gaps (no error triggered) | No |

The global and per-domain RMSD values (from `sup.rms`) and the mean pLDDT values are verified correct. The per-residue statistics and pocket RMSD (from scripts 062/064) should be discarded.
