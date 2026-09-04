
# Full ligand preparation in one cell — write files, no mol objects passed across
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors
import re, os, json

WORKDIR = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc'
SDF_IN  = "/home/ubuntu/rayca-artifacts/11507a0e2f5e69d5dfa40a62/files/P965_EDELRIS_2 Hits w enantiomers.sdf"

# Parse properties from original V3000
with open(SDF_IN) as f:
    raw = f.read()
blocks = raw.split('$$$$')
props_list = []
for blk in blocks:
    if not blk.strip(): continue
    p = {}
    for m in re.finditer(r'>  <([^>]+)>\s*\n([^\n]+)', blk):
        p[m.group(1).strip()] = m.group(2).strip()
    if p: props_list.append(p)

print(f"Property blocks: {len(props_list)}")

# Build mols from SMILES in properties (with stereo from 3D SDF via obabel V2000)
SDF_V2K = os.path.join(WORKDIR, 'ligands_v2000.sdf')
suppl = Chem.SDMolSupplier(SDF_V2K, removeHs=True, sanitize=True)
mols_raw = [m for m in suppl if m is not None]
print(f"Mols loaded: {len(mols_raw)}")

ligand_meta = []
lig_dir = os.path.join(WORKDIR, 'ligands')
os.makedirs(lig_dir, exist_ok=True)

for i, (mol, props) in enumerate(zip(mols_raw, props_list)):
    mol_id   = props.get('ID', f'lig{i}')
    mol_name = props.get('Molecule Name', f'Compound_{i}')
    kd       = props.get('Kd', '?')
    cls_val  = props.get('Class', '?')
    smiles_in = props.get('SMILES', '')

    # Canonical isomeric SMILES from 3D structure (preserves stereo)
    smi = Chem.MolToSmiles(mol, isomericSmiles=True)
    mw  = Descriptors.MolWt(mol)
    alogp = Descriptors.MolLogP(mol)
    hba = rdMolDescriptors.CalcNumHBA(mol)
    hbd = rdMolDescriptors.CalcNumHBD(mol)
    rot = rdMolDescriptors.CalcNumRotatableBonds(mol)
    stereo = Chem.FindMolChiralCenters(mol, includeUnassigned=True)

    # Add Hs and embed 3D conformer with ETKDG for docking
    mol_h = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol_h, AllChem.ETKDGv3())
    AllChem.MMFFOptimizeMolecule(mol_h)

    # Write SDF for this ligand
    sdf_path = os.path.join(lig_dir, f'{mol_id}.sdf')
    writer = Chem.SDWriter(sdf_path)
    writer.write(mol_h)
    writer.close()

    meta = {'id': mol_id, 'name': mol_name, 'kd': kd, 'cls': cls_val,
            'smiles': smi, 'smiles_orig': smiles_in,
            'mw': round(mw,1), 'logp': round(alogp,2),
            'hba': hba, 'hbd': hbd, 'rot': rot,
            'stereocenters': stereo, 'sdf': sdf_path}
    ligand_meta.append(meta)
    print(f"\n{mol_id} ({mol_name})")
    print(f"  Kd={kd}  MW={mw:.1f}  cLogP={alogp:.2f}  HBA={hba}  HBD={hbd}  Rot={rot}")
    print(f"  Stereocenters: {stereo}")
    print(f"  SMILES: {smi}")
    print(f"  Written: {sdf_path}  ({os.path.getsize(sdf_path)} bytes)")

# Save metadata
meta_path = os.path.join(WORKDIR, 'ligand_meta.json')
with open(meta_path, 'w') as f:
    json.dump([{k:v for k,v in m.items() if k != 'stereocenters'} for m in ligand_meta], f, indent=2)
print(f"\nMetadata saved: {meta_path}")
