
import re
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np

def fix_mol2_coords(lig):
    """Replace mol2 coordinates with docked-pose coords + properly-placed H."""
    mol2_path = PARAM_DIR / lig / f"{lig}.mol2"
    sdf_path  = LIG_DIR / f"{lig}_top.sdf"
    out_path  = PARAM_DIR / lig / f"{lig}_fixed.mol2"
    
    # 1. Load docked pose, add H with addCoords=True to preserve heavy-atom geometry
    mol_orig = next(Chem.SDMolSupplier(str(sdf_path), removeHs=False, sanitize=True))
    mol_noH  = Chem.RemoveHs(mol_orig)
    mol_allH = Chem.AddHs(mol_noH, addCoords=True)
    n_mol2_atoms = None
    
    # 2. Parse mol2 ATOM block to extract types, charges, names
    mol2_text = mol2_path.read_text()
    lines = mol2_text.split('\n')
    
    in_atom = False
    atom_records = []  # (idx, name, orig_x, orig_y, orig_z, atype, subst_id, subst_name, charge)
    for line in lines:
        if line.startswith('@<TRIPOS>ATOM'):
            in_atom = True; continue
        if line.startswith('@<TRIPOS>') and in_atom:
            in_atom = False
        if in_atom and line.strip():
            parts = line.split()
            atom_records.append(parts)
    
    n_mol2 = len(atom_records)
    n_sdf  = mol_allH.GetNumAtoms()
    
    if n_mol2 != n_sdf:
        return False, f"atom count mismatch: mol2={n_mol2} sdf={n_sdf}"
    
    # 3. Get SDF coordinates
    conf = mol_allH.GetConformer()
    coords = [conf.GetAtomPosition(i) for i in range(n_sdf)]
    
    # 4. Write new mol2 with replaced coords
    new_atom_block = []
    for i, rec in enumerate(atom_records):
        x, y, z = coords[i].x, coords[i].y, coords[i].z
        # rec = [id, name, x, y, z, type, subst_id, subst_name, charge]
        rec[2] = f"{x:10.4f}"
        rec[3] = f"{y:10.4f}"
        rec[4] = f"{z:10.4f}"
        new_atom_block.append('  '.join(rec))
    
    # Reconstruct mol2
    new_lines = []
    in_atom = False
    atom_inserted = False
    for line in lines:
        if line.startswith('@<TRIPOS>ATOM'):
            in_atom = True
            new_lines.append(line)
            for rec_line in new_atom_block:
                new_lines.append(rec_line)
            atom_inserted = True
            continue
        if line.startswith('@<TRIPOS>') and in_atom:
            in_atom = False
        if in_atom:
            continue  # skip old coords
        new_lines.append(line)
    
    out_path.write_text('\n'.join(new_lines))
    return True, f"n_atoms={n_mol2}"

print("Fixing mol2 coordinates to docked pose:")
results = {}
for lig in LIGS:
    ok, msg = fix_mol2_coords(lig)
    results[lig] = ok
    print(f"  {lig:<10}: {'OK' if ok else 'FAILED'} — {msg}")

print(f"\nAll fixed: {all(results.values())}")
