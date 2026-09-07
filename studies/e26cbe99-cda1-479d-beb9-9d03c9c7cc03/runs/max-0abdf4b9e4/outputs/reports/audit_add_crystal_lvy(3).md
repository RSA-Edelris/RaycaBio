# Audit: Add crystal ligand (LVY) to docking viewer

**Phase report:** `reports/phase_01_add_crystal_ligand_lvy_to_docking_viewer.md`  
**Artifacts checked:** `crystal_lvy.pdb`, `docking_viewer.html`, `source/048_open.py`, `source/049_js_str.py`, `source/050_open.py`  
**Auditor:** Independent verification agent  
**Date:** 2026-09-03

---

## Executive Summary

The phase succeeded in its core objective. All structural claims about the crystal ligand are correct, the 3Dmol.js API is used correctly, and all 10 functional checks verified by inspection of the actual files. One MAJOR finding concerns the imprecision of the HETATM count verification check. Three MINOR findings relate to dead code, session-state dependency, and a size claim inconsistency caused by post-write comment injection. No finding invalidates the result.

---

## Findings

### MAJOR — Imprecise HETATM verification check (050_open.py line 10)

**Code:**
```python
'19 LVY HETATM lines present':  h.count('HETATM') >= 19,
```

**Issue:** This counts *all* occurrences of the string `HETATM` anywhere in the HTML, not specifically the 19 LVY data lines. The HTML comment block at the top of `docking_viewer.html` (line 20 of the file) contains:
```
| CRYSTAL_LVY_PDB template literal embedded (19 HETATM lines) | PASS |
```
This contributes **1 extra occurrence** of the string `HETATM`. Measured result:

| Source | Count |
|:--|--:|
| HTML comment (lines 1–31) | 1 |
| Embedded `CRYSTAL_LVY_PDB` data | 19 |
| **Total `h.count('HETATM')`** | **20** |

Because the comment already contributes 1, the check `>= 19` would pass even if only **18** of the 19 LVY atoms were embedded (18 data + 1 comment = 19). A single dropped atom would go undetected. The check should instead count occurrences within the extracted `CRYSTAL_LVY_PDB` block, or use `== 19` on just the data section.

**Impact:** The check passed and the actual data is correct (19 lines confirmed), so the output is not wrong. But the check provides weaker guarantees than stated.

---

### MINOR — Dead variable `crystal_data` in 049_js_str.py (line 11)

**Code:**
```python
crystal_data = f'\nconst CRYSTAL_LVY_PDB = `{lvy_js}`;\n'   # line 11 — assigned, never used
h = h.replace(
    'const COMPOUNDS = ',
    'const CRYSTAL_LVY_PDB = `' + lvy_js + '`;\n\nconst COMPOUNDS = '   # lines 12-15
)
```

`crystal_data` is computed on line 11 but the actual replacement at lines 12–15 constructs the same string inline. `crystal_data` is never referenced again. No functional impact — the correct string is used — but if someone edits this code, `crystal_data` may create the false impression it is the value being inserted.

---

### MINOR — Cross-cell session dependency (049_js_str.py, 050_open.py)

`049_js_str.py` uses variables `lvy_pdb` (line 5) and `WD` (line 7) that are defined only in `048_open.py` (lines 2 and 22). `050_open.py` uses `WD` (line 4) also from `048_open.py`. These scripts are not self-contained; they fail with `NameError` if run standalone.

This is expected behaviour for the Modulon persistent-session model (cells share namespace). The risk is that if a single cell is re-run in isolation (e.g., during debugging), the dependency is invisible from the file itself.

---

### MINOR — File size discrepancy between embedded claim and current file

The HTML comment at line 27 states:  
`All 18 checks passed. File size: 285,018 bytes (278 KB).`

The actual current file size: **286,393 bytes** (≈280 KB).

The discrepancy is 1,375 bytes — consistent with the Modulon framework prepending the verification comment block (lines 1–31, which are 1,375 characters) to the HTML *after* `os.path.getsize()` was called in `050_open.py`. The size was accurate at verification time; the comment injection added to the file afterward. Not a bug, but any reader comparing the stated size to the current file will see a mismatch.

---

## Verification

Each item below was checked against the actual files, with evidence cited.

| Claim | Evidence | Status |
|:--|:--|:--|
| crystal_lvy.pdb contains exactly 19 HETATM lines | `wc -l crystal_lvy.pdb` = 20 lines (19 HETATM + `END`); confirmed by re-running extraction logic on raw PDB | VERIFIED CORRECT |
| All atoms have residue name LVY | Every line 1–19 of `crystal_lvy.pdb` reads `LVY` at `line[17:20]` | VERIFIED CORRECT |
| Chain B, residue 1429 | Columns 21 and 22–26 of every HETATM: `B`, `1429` | VERIFIED CORRECT |
| Atom composition C13 N3 O3 (19 heavy atoms, no H) | Counted from `crystal_lvy.pdb`: C1–C4, C6–C9, C11–C15 = 13 C; N5, N10, N17 = 3 N; O16, O18, O19 = 3 O. Total = 19 | VERIFIED CORRECT |
| No CONECT records for LVY in PDB 4CI2 | `conect_lines = []` confirmed by re-running 048 logic on `PB-20260903-4CI2_raw.pdb`: 0 CONECT records | VERIFIED CORRECT |
| CRYSTAL_LVY_PDB embedded in HTML | `docking_viewer.html` lines 5165–5183: 19 HETATM lines match `crystal_lvy.pdb` byte-for-byte | VERIFIED CORRECT |
| White sticks, color `#ffffff`, radius 0.12 | `docking_viewer.html` lines 5359, 5477–5478: `stick: { color: '#ffffff', radius: 0.12, opacity: 0.70 }` in both `rebuildScene()` and `toggleCrystal()` | VERIFIED CORRECT |
| `crystalModel = null` and `showCrystal = true` state variables | Lines 5233–5234 of `docking_viewer.html` | VERIFIED CORRECT |
| `crystalModel` reset to null at start of `rebuildScene()` | Line 5315: `crystalModel   = null;` inside `rebuildScene()` before reload | VERIFIED CORRECT |
| Crystal loaded in `rebuildScene()` when `showCrystal` is true | Lines 5356–5360 of `docking_viewer.html` | VERIFIED CORRECT |
| `viewer.render()` called after crystal load in `rebuildScene()` | Line 5364: `viewer.render();` follows immediately after `viewer.zoomTo(...)` which follows the crystal block | VERIFIED CORRECT |
| `toggleCrystal()` function exists with `removeModel` on toggle-off | Lines 5470–5487 of `docking_viewer.html`; `viewer.removeModel(crystalModel)` at line 5483; `viewer.render()` at line 5487 | VERIFIED CORRECT |
| `btn-crystal` button present with `onclick="toggleCrystal()"` | Line 249 of `docking_viewer.html` | VERIFIED CORRECT |
| Sidebar legend updated | Line 213: `<b style="color:#ffffff">White sticks</b> = LVY crystal ref` | VERIFIED CORRECT |
| PDB residue name parsing `line[17:20]` is correct | PDB format: residue name occupies 1-based columns 18–20 = 0-based indices 17:20. Confirmed against actual line: `line[17:20]` = `'LVY'` | VERIFIED CORRECT |
| `viewer.addModel(CRYSTAL_LVY_PDB, 'pdb')` argument order correct | 3Dmol.js signature: `addModel(data, type, options)`. Data first, format string second. Consistent with all other `addModel` calls in the same file (lines 5321, 5332, 5357, 5476) | VERIFIED CORRECT |
| `viewer.setStyle({model: crystalModel}, styleObj)` API form valid | `{model: glModelObject}` selection form is used identically for `receptorModel` (line 5322) and all 5 pose models (line 5335), which were verified working in the prior phase. Same pattern in this phase (lines 5358, 5477) | VERIFIED CORRECT |
| Receptor PDB has zero HETATM records | `grep -c HETATM PB-20260903-4CI2_receptor_trimmed_fixed.pdb` = 0. Confirms the HETATM count check is effectively counting only LVY atoms (plus the 1 in the comment) | VERIFIED CORRECT |
| `js_str()` escaping has no effect on PDB data | PDB files contain no backslash, backtick, or `${` sequences. `js_str(lvy_pdb) == lvy_pdb` confirmed by code evaluation | VERIFIED CORRECT |

---

## Riskiest Assumption in This Code

The single riskiest assumption is in `048_open.py` — that **all LVY atoms in the raw PDB belong to a single chain/residue combination and none are alternate conformations**. The code filters by residue name `LVY` only:

```python
if rec == 'HETATM' and line[17:20].strip() == 'LVY':
    lvy_lines.append(line)
```

It does not filter by chain ID or residue sequence number. If the raw PDB contained LVY molecules in two chains (the report acknowledges "one additional LVY molecule may exist in another chain"), both would be included. In practice, `PB-20260903-4CI2_raw.pdb` contains only one LVY molecule (19 atoms confirmed), so the assumption holds for this input. But the code would silently produce a 38-atom file for a two-chain structure, and 3Dmol.js would render both without error.

---

## Code-Level Checks: 048, 049, 050

### 048_open.py — LVY extraction

| Check | Finding |
|:--|:--|
| PDB column parsing `line[17:20]` for residue name | Correct (0-based Python vs 1-based PDB columns 18–20) |
| PDB column `line[6:11]` for serial number | Correct (PDB columns 7–11) |
| CONECT filter: `any(int(p) in lvy_serials for p in parts if p.isdigit())` | Correct; guards against non-digit tokens in CONECT lines; no bare except |
| No chain/residue filter on HETATM extraction | Assumption (see above); safe for this input, fragile for multi-chain LVY |
| Output file explicitly written to `crystal_lvy.pdb` | Confirmed |

### 049_js_str.py — HTML patching

| Check | Finding |
|:--|:--|
| `js_str()` escaping function | Correct; handles `\`, `` ` ``, `${`; no effect on PDB data |
| `crystal_data` on line 11 | Dead variable — assigned but never read |
| `h.replace('const COMPOUNDS = ', ...)` | Correct; inserts the crystal constant immediately before `COMPOUNDS`. Replace is deterministic because `const COMPOUNDS = ` is unique in the file |
| Assertions at end (lines 117–121) | Solid; no bare except; would raise `AssertionError` on failure |
| `WD` and `lvy_pdb` taken from prior cell | Session-dependency (see MINOR finding above) |

### 050_open.py — Verification

| Check | Finding |
|:--|:--|
| `h.count('HETATM') >= 19` | Imprecise (see MAJOR finding above) |
| All other 9 checks (substring presence) | Appropriate and distinct; no overlap that would allow a false positive |
| `finish(doc)` at line 77 | Platform-provided function; not in this file's scope but not a bug |
| `os.path.getsize()` result reported | Accurate at time of call; 1,375 bytes added afterward by framework comment injection |

---

## Conclusion

The phase output is correct. The 19-atom LVY crystal structure is accurately extracted, properly embedded, and correctly styled and controlled in the viewer. The 3Dmol.js API usage matches the installed CDN build and is consistent with the prior working viewer. The one MAJOR finding (weak HETATM check) does not affect the output, only the confidence in that specific verification step. No index confusion, no reversed arguments, no silent failure path, no wrong API version were found.
