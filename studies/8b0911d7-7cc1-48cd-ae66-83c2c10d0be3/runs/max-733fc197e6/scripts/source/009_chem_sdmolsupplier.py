
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors

suppl = Chem.SDMolSupplier(SDF_V2K, removeHs=False, sanitize=True)
mols_raw = [m for m in suppl if m is not None]
print(f"Loaded {len(mols_raw)} molecules")

# Also parse original V3000 to get SD properties (obabel may drop them)
# Read raw SDF to extract properties per molecule block
import re

with open(SDF_IN) as f:
    raw = f.read()

blocks = raw.split('$$$$')
props_list = []
for blk in blocks:
    if not blk.strip():
        continue
    p = {}
    for m in re.finditer(r'>  <([^>]+)>\s*\n([^\n]+)', blk):
        p[m.group(1).strip()] = m.group(2).strip()
    if p:
        props_list.append(p)

print(f"\nParsed {len(props_list)} property blocks")
for i, p in enumerate(props_list):
    print(f"  [{i}] ID={p.get('ID','?')} Name={p.get('Molecule Name','?')} Kd={p.get('Kd','?')} Class={p.get('Class','?')}")

# Map props onto RDKit mols
ligand_info = []
for i, (mol, props) in enumerate(zip(mols_raw, props_list)):
    mol_id   = props.get('ID', f'lig{i}')
    mol_name = props.get('Molecule Name', f'Compound_{i}')
    kd       = props.get('Kd', '?')
    cls_val  = props.get('Class', '?')
    smi_in   = props.get('SMILES', '')
    
    # Use RDKit canonical SMILES from 3D structure
    mol_noh = Chem.RemoveHs(mol)
    smi = Chem.MolToSmiles(mol_noh, isomericSmiles=True)
    mw  = Descriptors.MolWt(mol_noh)
    alogp = Descriptors.MolLogP(mol_noh)
    hba = rdMolDescriptors.CalcNumHBA(mol_noh)
    hbd = rdMolDescriptors.CalcNumHBD(mol_noh)
    rot = rdMolDescriptors.CalcNumRotatableBonds(mol_noh)
    stereo = Chem.FindMolChiralCenters(mol_noh, includeUnassigned=True)
    
    ligand_info.append({'id': mol_id, 'name': mol_name, 'kd': kd, 'cls': cls_val,
                        'smiles': smi, 'smiles_in': smi_in,
                        'mw': mw, 'logp': alogp, 'hba': hba, 'hbd': hbd, 'rot': rot,
                        'stereo': stereo, 'mol': mol, 'mol_noh': mol_noh})
    print(f"\n{mol_id} ({mol_name})  Kd={kd}  Class={cls_val}")
    print(f"  MW={mw:.1f}  cLogP={alogp:.2f}  HBA={hba}  HBD={hbd}  Rot={rot}")
    print(f"  Stereocenters: {stereo}")
    print(f"  SMILES: {smi}")
