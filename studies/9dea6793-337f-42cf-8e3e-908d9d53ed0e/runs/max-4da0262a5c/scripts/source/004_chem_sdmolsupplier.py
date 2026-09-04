
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, Draw, AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import os

sdf_path = "/home/ubuntu/rayca-artifacts/dc0c221c42d47c64e9717502/files/PoC Retrosynthetic analysis_Targets.sdf"
suppl_t = Chem.SDMolSupplier(sdf_path, removeHs=False, sanitize=True)

test_mols = {}
for mol in suppl_t:
    if mol is not None:
        name = mol.GetProp('_Name')
        if name.startswith('test_') or name == 'ED106680':
            smi = Chem.MolToSmiles(mol)
            formula = rdMolDescriptors.CalcMolFormula(mol)
            mw = Descriptors.MolWt(mol)
            rings = rdMolDescriptors.CalcNumRings(mol)
            arom = rdMolDescriptors.CalcNumAromaticRings(mol)
            stereo = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
            hbd = rdMolDescriptors.CalcNumHBD(mol)
            hba = rdMolDescriptors.CalcNumHBA(mol)
            rotb = rdMolDescriptors.CalcNumRotatableBonds(mol)
            test_mols[name] = {
                'smi': smi, 'formula': formula, 'mw': round(mw,1),
                'rings': rings, 'arom_rings': arom, 'stereocenters': len(stereo),
                'stereo_detail': stereo, 'hbd': hbd, 'hba': hba, 'rotb': rotb
            }
            print(f"\n{name}")
            print(f"  Formula: {formula}, MW: {round(mw,1)}")
            print(f"  SMILES: {smi}")
            print(f"  Rings: {rings} (aromatic: {arom})")
            print(f"  Stereocenters: {len(stereo)} — {stereo}")
            print(f"  HBD/HBA/RotBonds: {hbd}/{hba}/{rotb}")
