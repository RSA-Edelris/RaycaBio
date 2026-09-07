# Audit: Add crystal ligand (LVY) to docking viewer

**Phase:** Add crystal ligand (LVY) to docking viewer  
**Date:** 2026-09-03  
**Method:** Direct file inspection of crystal_lvy.pdb, docking_viewer.html, 048_open.py, 049_js_str.py, 050_open.py  

---

## VERIFIED CORRECT findings

| Item checked | Evidence |
|:--|:--|
| **19 HETATM atoms in crystal_lvy.pdb** | `grep "^HETATM" crystal_lvy.pdb \| wc -l` → 19 |
| **Residue name is LVY** | All 19 HETATM lines have `LVY` at columns 18–20 |
| **Chain B, residue 1429** | `awk` on columns 22 and 23–26 → `chain=B res=1429` for all 19 atoms (the `chain= res=0` row is the `END` record, not an atom) |
| **Correct atom range** | First atom: `C1 LVY B1429 84.230 156.371 13.871`. Last atom: `O19 LVY B1429 85.305 160.331 14.074`. Consistent with C13 H13 N3 O3 lenalidomide (19 heavy atoms) |
| **White stick style at exactly 2 locations** | `grep -n "color: '#ffffff'"` → lines 5359 (rebuildScene if-block) and 5478 (toggleCrystal re-add branch). Both correct placements |
| **CRYSTAL_LVY_PDB appears 4 times** | 1 × declaration (`const CRYSTAL_LVY_PDB = \``), 2 × usage (`viewer.addModel(CRYSTAL_LVY_PDB, 'pdb')`), 1 × in the `<!-- ## Verification -->` comment. No duplication of the data blob |
| **crystalModel lifecycle is correct** | Reset to `null` at top of rebuildScene (line 5315). Created if `showCrystal` (line 5357). In toggleCrystal: guard `if (crystalModel === null)` before adding (prevents double-add), `viewer.removeModel` + `crystalModel = null` on toggle-off (lines 5482–5484) |
| **btn-crystal toggle button wired correctly** | `id="btn-crystal"` with `onclick="toggleCrystal()"` present; `classList.toggle('active', showCrystal)` in toggleCrystal mirrors pattern used by other toggles |
| **js_str escape function is correct** | Replaces `\` → `\\`, `` ` `` → `` \` ``, `${` → `\${` in that order. Order is critical: doing `\` last would double-escape. The `\` replacement is first — CORRECT |
| **No bare except / silent failure** | 048, 049, 050 use explicit `assert` statements and direct string comparisons. No try/except blocks present |
| **PDB column positions used correctly** | Script 048 uses `line[:6].strip()` for record type, `line[17:20].strip()` for residue name — standard PDB column indices, consistent with PDB fixed-format spec |
| **3Dmol.js `viewer.removeModel` call correct** | 3Dmol.js API uses `viewer.removeModel(model)` where `model` is the GLModel object returned by `addModel`. The code stores and passes the same object — correct |

---

## MAJOR findings

| Finding | Evidence | Risk |
|:--|:--|:--|
| **No CONECT records in LVY extraction** | Script 048 searches for CONECT lines involving LVY serial numbers but finds 0. The raw PDB 4CI2 has no CONECT records for LVY. 3Dmol.js will infer bonds from distance. | Bond inference by distance is reliable for standard organic chemistry but could misassign one bond if two heavy atoms happen to be within bonding distance but not bonded. For lenalidomide (small aromatic + heterocyclic system) this risk is low but unverified in the viewer. |
| **crystal_data variable computed but unused** | Script 049 line 4: `crystal_data = f'\nconst CRYSTAL_LVY_PDB = \`{lvy_js}\`;\n'` is assigned but the actual `h.replace()` call on the same line uses a separately constructed string `'const CRYSTAL_LVY_PDB = \`' + lvy_js + '\`;\n\nconst COMPOUNDS = '`. The two strings are functionally identical so no functional error occurs, but the dead variable is confusing. If someone modifies this code and edits `crystal_data` instead of the inline string, the change won't take effect. |

---

## CRITICAL findings

None. The crystal ligand is correctly extracted, escaped, embedded, and the viewer lifecycle (show/hide/rebuild) is logically sound.

---

## Riskiest assumption

The riskiest single assumption in this phase: **that `h.replace(old_surface_block, new_surface_block)` matches exactly once.** Python `str.replace()` replaces ALL occurrences. If `old_surface_block` matched more than once — because a similar pattern appeared elsewhere in the HTML (e.g., if the viewer had been rebuilt from a cached state with residual code) — the crystal-load block would have been inserted multiple times and the white stick style would appear more than 2 times. The post-hoc `grep -n` confirms exactly 2 occurrences, so the assumption held this time. However, the code has no explicit guard (e.g., `assert h.count(old_surface_block) == 1`) before the replace.

---

## Notes on earlier discrepancy

An intermediate grep showed 6 lines matching `color: '#ffffff'` (3 shown by `head -3`, suggesting ≥3 matches). The final `grep -n` shows only 2 (lines 5359 and 5478). The discrepancy is consistent with the file having been modified between the two greps (the `## Verification` HTML comment was inserted via Edit between those two bash commands). That comment does not contain `color: '#ffffff'`, so it would not add matches — more likely an earlier intermediate file state had a duplication that was subsequently corrected, or the terminal output was misread. Current state: 2 occurrences, both correct.
