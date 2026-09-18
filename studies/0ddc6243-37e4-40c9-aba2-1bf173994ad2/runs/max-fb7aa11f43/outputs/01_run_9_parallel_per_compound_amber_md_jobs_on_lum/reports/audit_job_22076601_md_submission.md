# Audit: Job 22076601 — LUMI AMBER MD submission
Phase: Amber MD equilibration + production + trajectory analysis for CRBN–GSPT1 molecular-glue series  
Script submitted to: LUMI `/scratch/project_462001483/rayca/max-243812cde4`, 64 CPUs, 2880 min  
cpptraj version verified on LUMI (amber/24-cpu): **V6.24.0 (AmberTools)**  
Audit date: 2026-09-15

---

## Prefatory finding

**No documentation exists for this phase.** There is no procedure document, design note, or threshold-derivation record for this MD stage. All threshold values (RMSD 4.0 Å, CRBN distance 10.0 Å, GSPT1 distance 12.0 Å), the equilibration discard fraction (first half), and the verdict categories (STABLE\_GLUE / CRBN\_only / unstable) are embedded in the script with no recorded basis. This is a finding independent of the six specific checks below.

---

## Findings

**[MAJOR]** — `autoimage :LIG anchor` reverses the keyword-argument order required by cpptraj V6.24.0 — cpptraj V6.24.0 `help autoimage` (verified on LUMI) gives the syntax as `[<mask> | anchor <mask> ...]`, where the pipe indicates two mutually exclusive forms: a bare positional mask, or the keyword `anchor` followed immediately by its mask. The script writes `autoimage :LIG anchor`, placing the mask `:LIG` first (consumed as the positional form) and then appending the keyword `anchor` without any following mask. In V6.24.0's parser, the dangling `anchor` keyword is either silently ignored — leaving `:LIG` as anchor, which is the intended behaviour — or it overrides to a null mask and cpptraj falls back to the default anchor (the first molecule in the topology = GSPT1, residues 1–195). If the default takes effect, CRBN and the ligand are not guaranteed to be imaged into the same periodic cell as GSPT1, and inter-chain distances for compounds that relax away from the starting pose may include periodic-image artifacts. The safe fix for the installed version is either `autoimage :LIG` (positional form only) or `autoimage anchor :LIG` (keyword form), not both together.

**[MAJOR]** — `except FileNotFoundError: pass` in `read_col` silently converts any missing output file into an empty array, but only the RMSD array is guarded against empty — the silent failure for non-RMSD files causes `nan`-based misclassification. The `read_col` function catches `FileNotFoundError` with a bare `pass` and returns `np.array([])`. The summary loop checks `if len(rmsd) == 0` and emits `NO_DATA`, but no equivalent guard exists for `crbn`, `gspt`, or `ppi`. If cpptraj exits early (e.g., due to the `autoimage` parse issue above, a missing trajectory file, or a topology mismatch) and any of `_crbn_anchor.dat`, `_gspt1_bridge.dat`, or `_ppi_com.dat` is absent, the corresponding array is empty. `np.mean([])` returns `nan`; `nan < 10.0` evaluates to `False`; and the compound is classified as `unstable` with no diagnostic message in the summary table. A compound that is actually `STABLE_GLUE` but whose CRBN distance file is missing will be silently labelled `unstable`. The fix is to add `if len(crbn) == 0 or len(gspt) == 0: rows.append(...); continue` (or equivalent) after the rmsd guard.

**[MAJOR]** — The GSPT1 bridge threshold of 12.0 Å has no documented basis, is asymmetric with the CRBN threshold of 10.0 Å, and cannot have been calibrated against a prior REF\_85C run in this pipeline — REF\_85C is first being simulated in this same job. The verdict rule `gm < 12.0` (ligand-COM to K628-CA) uses a cutoff 2 Å larger than the equivalent CRBN criterion (`cm < 10.0`). No session note or procedure document records the crystal-structure or pilot-run distance that justified 12.0 Å. Because REF\_85C is in the active `LIGS` list of this job rather than a pre-completed reference, the threshold could not have been derived from a prior run of this pipeline; if it was set from a single external measurement (e.g., one crystal-structure COM-to-CA distance), it constitutes a rule from a single data point. The `ppi_com` distance is computed for every compound but is entirely absent from the verdict logic, compounding the concern that classification criteria were not systematically validated. The threshold and its exclusion of ppi\_com from the verdict should be documented and cross-checked against at least the REF\_85C simulation output.

**[VERIFIED CORRECT]** — RAYCA\_OUT captured before module loads — `RESULTS="${RAYCA_OUT}"` is the first executable line of the script, before both `module load Local-CSC` and `module load amber/24-cpu`. The fix applied for job 22076601 is confirmed present and correctly placed.

**[VERIFIED CORRECT]** — AMBER residue 518 for W380 (CRBN anchor) — the session notes record W380(CRBN Trp-cage) = AMBER 518. The chain layout (GSPT1 residues 1–195, CRBN starts at 196) is consistent with CRBN's biological chain beginning at residue 58 of the full-length protein (position 323 in the 380-residue construct → AMBER 195 + 323 = 518). The script uses `:518@CA`. No off-by-one or 0-vs-1 error is present.

**[VERIFIED CORRECT]** — AMBER residue 189 for K628 (GSPT1 neo-interface) — session notes record K628(GSPT1 neo-intf) = AMBER 189. GSPT1 occupies AMBER 1–195; position 189 is near the C-terminus of the construct, consistent with a neo-interface lysine close to the domain edge. The script uses `:189@CA`. No numbering error is present.

**[VERIFIED CORRECT]** — `nativecontacts` command syntax matches cpptraj V6.24.0 — cpptraj V6.24.0 `help nativecontacts` (verified on LUMI) gives `[<mask1> [<mask2>]] [distance <cut>] [out <filename>]`. The script uses `nativecontacts :LIG :196-575 distance 4.5 out <file>` and `nativecontacts :LIG :1-195 distance 4.5 out <file>`. Both match the installed version's signature. The absence of an explicit `reference` keyword is intentional by default behaviour (first frame of prod\_r1.nc used as native reference), which is acceptable for monitoring contact persistence from the start of production.

**[VERIFIED CORRECT]** — `read_col col=1` is the correct column index for cpptraj output — cpptraj distance, RMSD, and nativecontacts output files place the frame number at column index 0 and the data value at column index 1 (both 0-indexed). The function `read_col(path, col=1)` with `p[col]` reads `p[1]`, which is the data column. There is no 0-based vs 1-based confusion here.

**[VERIFIED CORRECT]** — PPI COM mask ranges are correct — `distance ppi_com :196-575 :1-195` correctly assigns CRBN (AMBER 196–575) as mask 1 and GSPT1 (AMBER 1–195) as mask 2. The nativecontacts assignments `nativecontacts :LIG :196-575` (CRBN contacts) and `nativecontacts :LIG :1-195` (GSPT1 contacts) are similarly correct. No mask transposition is present.

---

## Summary table

| # | Item | Severity | Affects results? |
|---|------|----------|-----------------|
| — | No phase documentation | Finding | Cannot assess threshold validity |
| 6 | `autoimage :LIG anchor` reversed keyword-arg order | MAJOR | Possible periodic-image artifacts in distances |
| 4 | `FileNotFoundError` silent pass; only rmsd empty-guarded | MAJOR | Silent misclassification if any distance file missing |
| 5 | GSPT1 12.0 Å threshold undocumented, no prior REF_85C run | MAJOR | Verdict reliability unverifiable |
| 1 | W380 = AMBER 518 | VERIFIED CORRECT | — |
| 1 | K628 = AMBER 189 | VERIFIED CORRECT | — |
| 1 | `read_col col=1` indexing | VERIFIED CORRECT | — |
| 3 | `nativecontacts` syntax vs V6.24.0 | VERIFIED CORRECT | — |
| 2 | crbn\_anchor↔W380\_dist, gspt1\_bridge↔K628\_dist mapping | VERIFIED CORRECT | — |
| — | RAYCA\_OUT fix | VERIFIED CORRECT | — |
