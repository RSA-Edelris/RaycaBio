
from rdkit import Chem
from rdkit.Chem import AllChem

def fix_mol2_coords(lig):
    mol2_path = PARAM_DIR / lig / f"{lig}.mol2"
    sdf_path  = LIG_DIR / f"{lig}_top.sdf"
    out_path  = PARAM_DIR / lig / f"{lig}_fixed.mol2"

    # Parse mol2 ATOM block
    mol2_text = mol2_path.read_text()
    lines = mol2_text.split('\n')
    in_atom, atom_records = False, []
    for line in lines:
        if line.startswith('@<TRIPOS>ATOM'):
            in_atom = True; continue
        if line.startswith('@<TRIPOS>') and in_atom:
            in_atom = False
        if in_atom and line.strip():
            atom_records.append(line.split())
    n_mol2 = len(atom_records)

    # Build geometry-correct molecule
    mol_orig = next(Chem.SDMolSupplier(str(sdf_path), removeHs=False, sanitize=True))
    n_orig   = mol_orig.GetNumAtoms()

    if n_orig == n_mol2:
        # Original SDF has matching atom count — use directly
        mol_use = mol_orig
        source = "original_SDF"
    else:
        # Add H while preserving heavy-atom docked-pose coordinates
        mol_noH  = Chem.RemoveHs(mol_orig)
        mol_allH = Chem.AddHs(mol_noH, addCoords=True)
        if mol_allH.GetNumAtoms() != n_mol2:
            return False, f"still mismatched: mol2={n_mol2} sdf+H={mol_allH.GetNumAtoms()}"
        mol_use = mol_allH
        source = "addCoords=True"

    conf   = mol_use.GetConformer()
    coords = [conf.GetAtomPosition(i) for i in range(n_mol2)]

    new_atom_lines = []
    for i, rec in enumerate(atom_records):
        x, y, z = coords[i].x, coords[i].y, coords[i].z
        new_line = f"{rec[0]:>7s} {rec[1]:<8s} {x:10.4f} {y:10.4f} {z:10.4f}  {rec[5]:<8s} {rec[6]:>2s} {rec[7]:<12s} {rec[8]:>10s}"
        new_atom_lines.append(new_line)

    new_lines, in_atom = [], False
    for line in lines:
        if line.startswith('@<TRIPOS>ATOM'):
            in_atom = True
            new_lines.append(line)
            new_lines.extend(new_atom_lines)
            continue
        if line.startswith('@<TRIPOS>') and in_atom:
            in_atom = False
        if in_atom:
            continue
        new_lines.append(line)

    out_path.write_text('\n'.join(new_lines))
    return True, f"n_atoms={n_mol2}  source={source}"

print("Fixing mol2 coordinates:")
results = {}
for lig in LIGS:
    ok, msg = fix_mol2_coords(lig)
    results[lig] = ok
    print(f"  {lig:<10}: {'OK' if ok else 'FAILED'} — {msg}")

print(f"\nAll fixed: {all(results.values())}")
