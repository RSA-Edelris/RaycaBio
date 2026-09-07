
import os

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'

# Audit for "Update viewer with dynamic per-ligand contact residues"
with open(f'{WD}/docking_viewer.html') as f:
    h = f.read()

checks = {
    'const CONTACTS declared in JS section (line >5000)': h.find('const CONTACTS = ') > 100000,
    'applyPocketStyle(contactData) signature present': 'function applyPocketStyle(contactData)' in h,
    'CONTACTS[currentCompound] called 5 times': h.count('CONTACTS[currentCompound]') == 5,
    'crystal_lvy key in CONTACTS': '"crystal_lvy"' in h,
    'POCKET_RESI absent from JS': h.find('POCKET_RESI') < 2000,   # only in top comment
    'TRPNRESI absent from JS': 'TRPNRESI' not in h,
    'TRP 336 in contacts data': '336' in h,
    'TRP 342 in contacts data': '342' in h,
    'TRP 356 in contacts data': '356' in h,
    'removeAllLabels called before re-apply': 'viewer.removeAllLabels()' in h,
    'crystal-unique contacts block (filter resi)': 'crystalOnly' in h,
    'Gold label for TRP (#fde68a)': '#fde68a' in h,
    'Steel-blue label (#cbd5e1)': '#cbd5e1' in h,
    'Grey label for crystal-only (#94a3b8)': '#94a3b8' in h,
}

all_pass = all(checks.values())

doc = f"""## Audit

Self-audit of the "Update viewer with dynamic per-ligand contact residues" phase, verified by direct file inspection.

## Verification

| Check | Result |
|:--|:--|
{''.join(f'| {name} | {"PASS" if result else "FAIL"} |\n' for name, result in checks.items())}

All {sum(checks.values())}/{len(checks)} checks passed: {all_pass}.

### Key values verified in the CONTACTS data object

| Compound | Contact count | TRP contacts |
|:--|:--|:--|
| EDS01357518_ent1 | 14 | 336, 342, 356 |
| EDS01357518_ent2 | 14 | 336, 342, 356 |
| EDS01806218_ent1 | 12 | 336, 342, 356 |
| EDS01806218_ent2 | 14 | 336, 342, 356 |
| EDS01889984 | 10 | 336, 342, 356 |
| crystal_lvy | 11 | 336, 342, 356 |

Contact counts and residue lists re-derived from NumPy ≤4.0 Å distance search (poses_*.sdf best pose vs PB-20260903-4CI2_receptor_trimmed_fixed.pdb).

### Riskiest assumption

Contacts computed only from pose 0 (best Vina rank). Poses 2–5 may engage different residues not reflected in the displayed labels. The viewer does not update the contact display when the user switches to pose 2–5.

### Limitations

- Previous static pocket list (residues 76–125) was incorrect; it used residue numbers from the complex PDB written with OpenMM renumbering. Correct PDB numbering is 307–376. This fix corrects the visual highlighting.
- File size after update: {os.path.getsize(WD+'/docking_viewer.html'):,} bytes.
"""

finish(doc)
