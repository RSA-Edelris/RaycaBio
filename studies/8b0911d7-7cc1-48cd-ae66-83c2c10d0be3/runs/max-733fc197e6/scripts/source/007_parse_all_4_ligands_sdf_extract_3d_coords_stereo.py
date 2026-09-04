
# Parse all 4 ligands from SDF, extract 3D coords + stereo SMILES
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors
import os

SDF_IN = "/home/ubuntu/rayca-artifacts/11507a0e2f5e69d5dfa40a62/files/P965_EDELRIS_2 Hits w enantiomers.sdf"

# V3000 SDF - read with RDKit
suppl = Chem.SDMolSupplier(SDF_IN, removeHs=False, sanitize=True)
mols = [m for m in suppl if m is not None]
print(f"Loaded {len(mols)} molecules")

ligand_info = []
for mol in mols:
    mol_id   = mol.GetPropsAsDict().get('ID', mol.GetProp('_Name') if mol.HasProp('_Name') else '?')
    mol_name = mol.GetPropsAsDict().get('Molecule Name', '?')
    kd       = mol.GetPropsAsDict().get('Kd', '?')
    cls_val  = mol.GetPropsAsDict().get('Class', '?')
    smi      = Chem.MolToSmiles(mol, isomericSmiles=True)
    mw       = Descriptors.MolWt(mol)
    hba      = rdMolDescriptors.CalcNumHBA(mol)
    hbd      = rdMolDescriptors.CalcNumHBD(mol)
    rot      = rdMolDescriptors.CalcNumRotatableBonds(mol)
    alogp    = Descriptors.MolLogP(mol)
    stereo_info = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
    
    ligand_info.append({
        'id': mol_id, 'name': mol_name, 'kd': kd, 'cls': cls_val,
        'smiles': smi, 'mw': mw, 'hba': hba, 'hbd': hbd, 'rot': rot,
        'logp': alogp, 'stereocenters': stereo_info, 'mol': mol
    })
    print(f"\n{mol_id} ({mol_name})")
    print(f"  Kd={kd}  Class={cls_val}")
    print(f"  MW={mw:.1f}  cLogP={alogp:.2f}  HBA={hba}  HBD={hbd}  RotBonds={rot}")
    print(f"  Stereocenters: {stereo_info}")
    print(f"  SMILES: {smi[:80]}...")
