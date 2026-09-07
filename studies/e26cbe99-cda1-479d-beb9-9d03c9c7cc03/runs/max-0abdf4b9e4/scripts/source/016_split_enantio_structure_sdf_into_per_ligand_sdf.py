
from rdkit import Chem
from rdkit.Chem import SDWriter
import os

# ── Split enantio_structure.sdf into per-ligand SDF files ────────────────────
suppl = Chem.SDMolSupplier('enantio_structure.sdf', removeHs=False, sanitize=True)
lig_sdf_paths = []
for mol in suppl:
    if mol is None:
        continue
    name = mol.GetProp('_Name')
    path = f'lig_{name}.sdf'
    w = SDWriter(path)
    w.write(mol)
    w.close()
    lig_sdf_paths.append((name, path))
    print(f"  Wrote {path}  ({os.path.getsize(path):,} bytes)")

print(f"\n{len(lig_sdf_paths)} ligand files ready")
print(f"Receptor: {receptor_path}  ({os.path.getsize(receptor_path):,} bytes)")

# Docking box parameters
BOX_CTR = (pocket_cx, pocket_cy, pocket_cz)   # 84.80, 154.94, 13.24
BOX_SZ  = 25.0
print(f"\nDocking box centre: {BOX_CTR}  size: {BOX_SZ}×{BOX_SZ}×{BOX_SZ} Å")
