
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, AllChem
from rdkit.Chem import rdchem
import os

sdf_path = "/home/ubuntu/rayca-artifacts/dc0c221c42d47c64e9717502/files/PoC Retrosynthetic analysis_Targets.sdf"

suppl = Chem.SDMolSupplier(sdf_path, removeHs=False, sanitize=True)

compounds = []
for mol in suppl:
    if mol is not None:
        name = mol.GetProp('_Name') if mol.HasProp('_Name') else 'unnamed'
        smi = Chem.MolToSmiles(mol)
        mw = Descriptors.MolWt(mol)
        formula = rdMolDescriptors.CalcMolFormula(mol)
        rings = rdMolDescriptors.CalcNumRings(mol)
        arom = rdMolDescriptors.CalcNumAromaticRings(mol)
        stereocenters = len(Chem.FindMolChiralCenters(mol, includeUnassigned=True))
        natoms = mol.GetNumHeavyAtoms()
        compounds.append({
            'name': name,
            'smiles': smi,
            'MW': round(mw,1),
            'formula': formula,
            'Rings': rings,
            'ArRings': arom,
            'Stereocenters': stereocenters,
            'HeavyAtoms': natoms
        })
        print(f"{'='*60}")
        print(f"Name: {name}")
        print(f"Formula: {formula}  MW={round(mw,1)}")
        print(f"Rings={rings}, AromaticRings={arom}, Stereocenters={stereocenters}")
        print(f"SMILES: {smi}")
    else:
        print("Failed to parse a molecule")
