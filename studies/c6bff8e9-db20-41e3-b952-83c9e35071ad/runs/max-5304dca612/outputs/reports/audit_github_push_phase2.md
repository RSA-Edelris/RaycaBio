# Audit Report — "Push new files to RSA-Edelris/RaycaBio GitHub" Phase

**Auditor:** Independent reviewer (not involved in producing the outputs)
**Date audited:** 2026-09-16
**Scope:** `generate_platemap_fresh.py`, `generate_platemap_round2.py`,
`HTE_BH_fresh_standalone_4x2x12.md`, `audit_round2_phase.md`,
`phase_fix_audit_and_fresh_plate.md`

---

## Findings Summary

| # | Finding | Severity | File | Location |
|---|---|---|---|---|
| 1 | Phase document is an auto-generated shell with no method content | MAJOR | `reports/phase_01_push_new_files_to_rsa_edelris_raycabio_github.md` | Entire document |
| 2 | Assert in both generator scripts is vacuously true — cannot detect any design error | MAJOR | `generate_platemap_fresh.py`, `generate_platemap_round2.py` | Lines 55–56; Lines 54–55 |
| 3 | "PEPSI" label (missing one P) unfixed in both scripts and in fresh-plate markdown | MINOR | `generate_platemap_fresh.py` L31; `generate_platemap_round2.py` L30; `HTE_BH_fresh_standalone_4x2x12.md` L51 | Short-name field |
| — | All 12 CAS numbers in `generate_platemap_fresh.py` verified against SDF | VERIFIED CORRECT | `generate_platemap_fresh.py` | Lines 19–32 |
| — | matplotlib 3.11.1 confirmed; Circle and FancyBboxPatch signatures correct | VERIFIED CORRECT | Both scripts | All patch/circle calls |
| — | Argument order correct; x=column-index, y=row-index used consistently | VERIFIED CORRECT | Both scripts | Circle/FancyBboxPatch calls |
| — | No bare except, no `or []`, no `or {}`, no `getattr(..., default)` | VERIFIED CORRECT | Both scripts | Whole file |
| — | No `_F`-suffixed identifier confusion | VERIFIED CORRECT | `generate_platemap_fresh.py` | Whole file |
| — | No single-data-point rules in any markdown document | VERIFIED CORRECT | All three markdown files | — |
| — | 0-based/1-based indexing handled correctly | VERIFIED CORRECT | Both scripts | Column/row labelling loops |

---

## MAJOR FINDINGS

### MAJOR-1 — Phase document is an auto-generated shell; push procedure is entirely undocumented

**File:** `reports/phase_01_push_new_files_to_rsa_edelris_raycabio_github.md`

This document exists and is named exactly for the phase under audit, but contains no method content. It is a machine-generated template produced by "Rayca Modulon phase report." Its key statements:

> Line 41: "No method records were captured for this phase, so the procedure cannot be stated. This is a gap in the record, not a phase that did no work."
> Line 44: "This phase produced no captured result output."
> Line 96: "No tool call is on record for this phase."
> Line 101: "No method records were captured, so this phase cannot be reproduced from this report alone."

The document lists 41 artifact files (Table A) but records none of the following:
- Which commit hash and branch were used for the push.
- Which files were selected for push and why.
- What validation (CAS lookup, well-count check, visual inspection) was performed before committing.
- What the pre-push state of the repository was, or whether conflicts were resolved.

This is not equivalent to "no document." The document actively creates the appearance of a record while containing no auditable content. A reviewer who sees `reports/phase_01_push_new_files_to_rsa_edelris_raycabio_github.md` filed as the phase write-up will incorrectly believe the phase was documented.

For comparison, the Round 1 push has a human-written `push_phase_summary.md` in the session root that specifies commit `3cb732698d46d194c46f1828ee9c990b37183807`, branch `hte-bh-campaign-round1`, the 13 files committed, and validation steps. No equivalent exists for this push phase.

**Verdict:** MAJOR. The push phase for these new files is not documented. If pushed files are later found incorrect, there is no record of what state check, if any, preceded the commit.

---

### MAJOR-2 — Assert in `generate_platemap_fresh.py` (and `generate_platemap_round2.py`) is vacuously true; it cannot detect any design error

**File:** `generate_platemap_fresh.py`, lines 44–56

```python
grid_color = [[None]*12 for _ in range(8)]        # line 45 — hard-coded 8×12 = 96 cells
grid_label = [[None]*12 for _ in range(8)]

for ri in range(8):                                # line 48 — range fixed at 8
    sol_idx  = ri // 4
    base_idx = ri  % 4
    for ci in range(12):                           # line 51 — range fixed at 12
        grid_color[ri][ci] = CATALYSTS[ci][2]      # line 52 — hex string, always truthy
        grid_label[ri][ci] = (...)

total = sum(1 for r in range(8) for c in range(12) if grid_color[r][c])   # line 55
assert total == 96, f"Well count error: {total} ≠ 96"                     # line 56
```

`CATALYSTS[ci][2]` is always a non-empty hex color string such as `"#D62828"`. In Python, any non-empty string is truthy. The sum therefore counts every cell in the 8×12 grid unconditionally. The result is always exactly 96. The assert cannot fail.

The assert would need to guard against real failure modes — e.g., `CATALYSTS` having fewer than 12 entries, a row being duplicated, or a cell accidentally left None. None of those failures can reach the assert:

- If `CATALYSTS` has fewer than 12 entries, Python raises `IndexError` at line 52 before the assert is ever reached.
- The grid dimensions are hard-coded at 8 and 12 in both the initializer and the fill loop, so the cell count is structurally fixed at 96 regardless of the plate design.
- No code path sets any cell back to None after line 52.

The same structural problem exists identically in `generate_platemap_round2.py` lines 44–55.

**Verdict:** MAJOR. The assert provides false assurance. A design change that altered the number of bases, solvents, or catalysts without changing the hard-coded `range(8)` / `range(12)` bounds would produce a mis-designed plate with no runtime error. The assert is dead code dressed as a safety check.

**Fix required:** Either (a) replace the assert with explicit structural checks — `assert len(CATALYSTS) == 12`, `assert len(BASES) == 4`, `assert len(SOLVENTS) == 2` — or (b) derive the grid dimensions from the data rather than hard-coding them, so a miscount causes a real failure. The current approach does neither.

---

## MINOR FINDINGS

### MINOR-1 — "PEPSI" label (missing one P) unfixed in both generator scripts and in fresh-plate markdown

**Files:**
- `generate_platemap_fresh.py`, line 31: `("PEPPSI [NHC-Pd]", "PEPSI", "#E76F51", "1158652-41-5", "NHC")`
- `generate_platemap_round2.py`, line 30: `("PEPPSI [NHC-Pd]", "PEPSI", "#E76F51", "1158652-41-5", "NHC")`
- `HTE_BH_fresh_standalone_4x2x12.md`, line 51: `| 12 | **PEPSI** | **PEPPSI [NHC-Pd]** | ...`

The correct acronym is **PEPPSI** (Pyridine-Enhanced Precatalyst Preparation Stabilization and Initiation, 6 letters). The rendered plate map displays "PEPSI" on all 8 PEPPSI wells in column 12 and on the column 12 header chip. This was already flagged as MINOR-1 in `audit_round2_phase.md` for the round2 script. It was explicitly not corrected when `generate_platemap_round2.py` was written ("Typo carried forward as-is") and it was then re-introduced identically into `generate_platemap_fresh.py`.

The fix is one character: change `"PEPSI"` to `"PEPPSI"` at the three locations above and regenerate both PNGs.

**Verdict:** MINOR. Does not affect well assignment, CAS number, or scientific classification, but the label on every column-12 well in both plate images is incorrect and will propagate into any ELN entry that reads the image.

---

## VERIFIED CORRECT

### VERIFIED-1: All 12 CAS numbers in `generate_platemap_fresh.py` confirmed present in `HTE_Edelris.sdf`

All 12 catalysts declared in `generate_platemap_fresh.py` lines 19–32 were checked against the 74-entry Edelris SDF at `/home/ubuntu/rayca-artifacts/9b531d029532706a25e7a959/files/HTE_Edelris.sdf`.

| Col | Short | CAS claimed | SDF name |
|---|---|---|---|
| 1 | BPG3 | 1470372-59-8 | "(BrettPhos Pd G3)" ✓ |
| 2 | tBBG3 | 1536473-72-9 | "tBuBrettPhos Pd G3" ✓ |
| 3 | RuPG3 | 1445085-77-7 | "(RuPhos-Pd-G3)" ✓ |
| 4 | XPG3 | 1445085-55-1 | "(XPhos-Pd-G3)" ✓ |
| 5 | MorG3 | 2222690-89-1 | "(MorDalPhos-Pd-G3)" ✓ |
| 6 | PCy3 | 1445086-12-3 | "(PCy3-Pd-G3)" ✓ |
| 7 | XantG3 | 1445085-97-1 | "XantPhos Pd G3" ✓ |
| 8 | dppf | 1445086-28-1 | "(dppf-Pd-G3)" ✓ |
| 9 | BINAP | 2151915-22-7 | "(rac-BINAP-Pd-G3)" ✓ |
| 10 | CatA | 1651823-59-4 | "cataCXium-A-Pd-G3" ✓ |
| 11 | GPG3 | 2489525-82-6 | "GPhos-Pd-G3" ✓ |
| 12 | PEPSI | 1158652-41-5 | NHC-Pd / 3-chloropyridine complex ✓ |

All 12 found, no CAS number misattribution. The five catalysts not covered by the prior round2 audit (XPhos, BINAP, PCy3, XantPhos, GPhos) were specifically confirmed in this audit.

---

### VERIFIED-2: matplotlib 3.11.1 installed; Circle and FancyBboxPatch signatures are correct

Confirmed via `python3 -c "import matplotlib; print(matplotlib.__version__); import inspect; from matplotlib.patches import Circle, FancyBboxPatch; print(inspect.signature(Circle.__init__)); print(inspect.signature(FancyBboxPatch.__init__))"`:

```
3.11.1
Circle:         (self, xy, radius=5, **kwargs)
FancyBboxPatch: (self, xy, width, height, boxstyle='round', *, mutation_scale=1, mutation_aspect=1, **kwargs)
```

Every call in `generate_platemap_fresh.py` and `generate_platemap_round2.py` matches these signatures:

- `Circle((x, y), R, color=..., zorder=..., linewidth=0)` — positional `xy` then `radius`, remaining as kwargs. ✓
- `FancyBboxPatch((-0.5, y_bot), 12.0, 4.1, boxstyle="round,pad=0.15", ...)` — positional `xy`, `width`, `height`, then kwargs. ✓

No deprecated API calls. `matplotlib.use('Agg')`, `ax.axis('off')`, `plt.tight_layout()`, `plt.savefig(..., bbox_inches='tight', facecolor='white')` are all current as of matplotlib 3.11.1. No calls to removed parameters (e.g., `antialiased=` removed in 3.7 for some patches) were found.

---

### VERIFIED-3: Argument order correct; x = column-index, y = row-index throughout

`generate_platemap_fresh.py` lines 107–114:

```python
x, y  = float(ci), 7.0 - float(ri)
```

`ci` ranges 0–11 (left to right, matching columns 1–12).
`y = 7.0 - ri`: `ri=0` → y=7.0 (top, row A); `ri=7` → y=0.0 (bottom, row H).

The xlim/ylim are `(-2.2, 15.0)` and `(-1.8, 10.5)`, placing all 96 well circles within the visible area. `Circle((x,y), R, ...)` passes the center as `(x,y)` which is `(xy)` per the confirmed signature. No reversed x/y. `FancyBboxPatch` calls use the lower-left corner convention correctly; e.g., `FancyBboxPatch((-0.45, 7.0-ri-0.43), 11.9, 0.86, ...)` centres the row stripe at y = `7.0-ri` as expected.

---

### VERIFIED-4: No bare except, no `or []`, no `or {}`, no `getattr(..., default)`

Neither `generate_platemap_fresh.py` nor `generate_platemap_round2.py` contains any `try`/`except` block, any `variable or []` / `variable or {}` default idiom, or any `getattr(obj, attr, default)` call. Grep across both files confirms zero occurrences. The only error-handling mechanism is the `assert total == 96` guard discussed in MAJOR-2. Failure modes for missing files (`pathlib.Path(...) / "..."` then `plt.savefig(out, ...)`) will raise uncaught OSError/PermissionError as expected.

---

### VERIFIED-5: No `_F`-suffixed identifier confusion in `generate_platemap_fresh.py`

The question probes whether variables named `BASES_F`, `CATALYSTS_F`, or `SOLVENT_BG_F` are present and could be confused with their unsubscripted counterparts. They are not present. `generate_platemap_fresh.py` defines exactly one set of these names: `CATALYSTS` (line 19), `BASES` (line 35), `SOLVENTS` (line 37), `SOLVENT_BG` (line 41), `BASE_COLORS` (line 40). No `_F` variants exist anywhere in the file. Each name is used consistently at every call site.

---

### VERIFIED-6: No single-data-point rules in any markdown document

`HTE_BH_fresh_standalone_4x2x12.md`, `audit_round2_phase.md`, and `phase_fix_audit_and_fresh_plate.md` were each read in full. No statement takes the form "experiment X showed Y, therefore Y is always true." Every scientific claim is grounded in general chemical principles (pKa arguments for base selection, ε for solvent selection, established BH literature for catalyst rationale) or stated explicitly as a prediction. The document at line 4 of `HTE_BH_fresh_standalone_4x2x12.md` proactively declares: "This plate is designed entirely from chemical first principles. It makes no reference to data from any prior HTE plate." The analysis plan (section starting at line 122) contains instructions, not data-derived rules.

---

### VERIFIED-7: 0-based/1-based indexing correct; no off-by-one errors

In both generator scripts, `for ci in range(12)` maps ci=0 to column 1 and ci=11 to column 12. Column number labels use `str(ci+1)` (line 92 of `generate_platemap_fresh.py`; line 90 of `generate_platemap_round2.py`). `for ri in range(8)` maps ri=0 to row A and ri=7 to row H via `ROWS[ri]` (line 38 of fresh; line 36 of round2). Row base assignment uses `base_idx = ri % 4`, which for ri=0–7 cycles through 0,1,2,3,0,1,2,3 — correctly assigning bases to rows A–D and E–H. Solvent assignment uses `sol_idx = ri // 4`, producing 0 for rows A–D and 1 for rows E–H. No off-by-one errors found.

---

## Actions Required

1. **[BLOCKING] Write a substantive push-phase summary** covering: files pushed, commit hash, branch, pre-push validation steps. The machine-generated shell at `reports/phase_01_push_new_files_to_rsa_edelris_raycabio_github.md` does not satisfy this requirement.

2. **[BLOCKING] Replace the vacuous assert with real structural guards** in both `generate_platemap_fresh.py` and `generate_platemap_round2.py`. At minimum add: `assert len(CATALYSTS) == 12`, `assert len(BASES) == 4`, `assert len(SOLVENTS) == 2` before the grid-fill loop, and change the grid count check to use a sentinel that can actually be unset.

3. **[NON-BLOCKING] Correct "PEPSI" → "PEPPSI"** in `generate_platemap_fresh.py` line 31, `generate_platemap_round2.py` line 30, `HTE_BH_fresh_standalone_4x2x12.md` line 51, and regenerate both PNGs. This was carried forward unfixed from the prior audit.
