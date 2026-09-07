
from rdkit import Chem
import os

# ── 1. Strip H from receptor for fpocket ─────────────────────────────────────
receptor_noh_path = 'PB-20260903-4CI2_receptor_noH.pdb'
with open(receptor_path) as rf, open(receptor_noh_path, 'w') as wf:
    for line in rf:
        rec = line[:6].strip()
        if rec in ('ATOM', 'HETATM'):
            atom_name = line[12:16].strip()
            element   = line[76:78].strip() if len(line) > 76 else ''
            # skip hydrogen lines
            if atom_name.startswith('H') or element == 'H':
                continue
        wf.write(line)

print(f"H-stripped receptor: {receptor_noh_path}  "
      f"({os.path.getsize(receptor_noh_path):,} bytes)")

# ── 2. Extract SMILES from enantio_structure.sdf ─────────────────────────────
sdf_path = 'enantio_structure.sdf'
suppl = Chem.SDMolSupplier(sdf_path, removeHs=True, sanitize=True)
ligand_info = []
for mol in suppl:
    if mol is None:
        continue
    name = mol.GetProp('_Name')
    smi  = Chem.MolToSmiles(mol)
    ligand_info.append({'name': name, 'smiles': smi})
    print(f"  {name}: {smi}")

print(f"\nTotal ligands: {len(ligand_info)}")
