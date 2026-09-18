
# Step 1: Read SDF and inspect compounds
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors
import os

sdf_path = "/home/ubuntu/rayca-artifacts/eaff7adfa74be7523e4a94b7/files/CRBN_lig_results_2.sdf"
print(f"SDF size: {os.path.getsize(sdf_path):,} bytes")

suppl = Chem.SDMolSupplier(sdf_path, removeHs=False)
mols = [m for m in suppl if m is not None]
print(f"Molecules parsed: {len(mols)}")

for i, mol in enumerate(mols):
    props = mol.GetPropsAsDict()
    name = mol.GetProp('_Name') if mol.HasProp('_Name') else f"mol_{i}"
    mw   = round(Descriptors.MolWt(mol), 1)
    hba  = rdMolDescriptors.CalcNumHBA(mol)
    hbd  = rdMolDescriptors.CalcNumHBD(mol)
    rotb = rdMolDescriptors.CalcNumRotatableBonds(mol)
    rings = rdMolDescriptors.CalcNumRings(mol)
    smi  = Chem.MolToSmiles(Chem.RemoveHs(mol))
    score = props.get('score', props.get('affinity', props.get('docking_score', 'n/a')))
    print(f"  [{i}] {name:30s} MW={mw:6.1f}  HBA={hba} HBD={hbd} RotB={rotb} Rings={rings} score={score}")
    print(f"       SMILES: {smi[:90]}")
