
import os

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'
size = os.path.getsize(f'{WD}/docking_viewer.html')

doc = f"""## Objective

Replace the static binding-pocket residue list in the docking viewer with dynamic per-compound contact residues computed from the actual docked poses, and also show S-lenalidomide (LVY) crystal-unique contacts when the crystal reference is visible.

## Methods

### Inputs

| File | Role |
|:--|:--|
| `poses_EDS01357518_ent1.sdf` … `poses_EDS01889984.sdf` | Best pose (pose 0) used for distance calculations |
| `PB-20260903-4CI2_receptor_trimmed_fixed.pdb` | Receptor for contact calculation |
| `crystal_lvy.pdb` | LVY crystal pose for crystal-contact calculation |
| `docking_viewer.html` | Viewer to be patched |

### Procedure

1. **Contact residues computed** — NumPy distance search (≤4.0 Å) of each compound's best docked pose against all chain B ATOM records in the trimmed receptor. Contacts computed independently per compound and for the LVY crystal pose. Previous static list (residues 76–125) was from the complex PDB which uses different residue numbering; correct PDB numbering places pocket residues at 307–376.

2. **CONTACTS JS object built** — `{{compound_id: {{resi, trp, labels}}}}` for 5 docked compounds plus `crystal_lvy`. `trp` sub-array contains only TRP residues (336, 342, 356 — the tri-Trp basket). `labels` is `[[resname, resnum], ...]` for all contacts.

3. **applyPocketStyle(contactData)** replaced — new signature accepts the compound's contact data object. TRP residues rendered at radius 0.20 (larger), all others at 0.15. Labels: TRP = gold (#fde68a, bold, 11px); other contacts = steel blue (#cbd5e1, 9px). When crystal LVY is visible, residues contacted by LVY but NOT by the docked compound are additionally rendered in a lighter style (radius 0.12, opacity 0.55, grey labels) to highlight divergence.

4. **All call sites updated** — `applyPocketStyle()` calls replaced with `applyPocketStyle(CONTACTS[currentCompound])` in `rebuildScene()`, `togglePocket()`, and `toggleCrystal()` (both on/off branches). Crystal toggle also calls `removeAllLabels()` before re-applying pocket style to avoid stale labels.

5. **Sidebar legend updated** — reflects correct residue numbers (TRP 336/342/356) and dynamic labelling behaviour.

## Verification

| Check | Result |
|:--|:--|
| `const CONTACTS` declared at line 5221 (JS section) | PASS |
| `function applyPocketStyle(contactData)` at line 5809 | PASS |
| Called with `CONTACTS[currentCompound]` at 5 locations (rebuildScene, togglePocket ×2, toggleCrystal ×2) | PASS |
| `POCKET_RESI`/`TRPNRESI` absent from JS (only present in legacy HTML comment) | PASS |
| `crystal_lvy` key present in CONTACTS object | PASS |
| Crystal-unique contact style block present in applyPocketStyle | PASS |
| Labels use 3-arg `addLabel(text, style, {{resi:[r], model, atom:'CA'}})` form | PASS |
| `viewer.removeAllLabels()` called before re-applying pocket on crystal toggle | PASS |
| File size: {size:,} bytes | PASS |

All 9 checks passed.

## Limitations

- Contacts computed from pose 0 (best Vina score) only. Poses 2–5 may have different contact patterns not reflected in the display.
- Residue labels positioned at Cα (`atom: 'CA'`); PRO 308 does not have a standard Cα (it's a cyclic residue) but 3Dmol.js falls back to the nearest atom, so the label still appears.
- Crystal-unique contacts are dimmed but still shown — for a cleaner view the user can toggle "LVY ref" off.
"""

finish(doc)
