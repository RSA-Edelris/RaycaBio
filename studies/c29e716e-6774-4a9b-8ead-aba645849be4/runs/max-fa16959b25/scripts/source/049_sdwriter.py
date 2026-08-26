
from rdkit import Chem
from rdkit.Chem import SDWriter, AllChem, Descriptors
import os

out_path = "/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02/P841_proposed_20.sdf"

writer = SDWriter(out_path)
for pid, smi, rationale in proposals_v2:
    mol = Chem.MolFromSmiles(smi)
    AllChem.Compute2DCoords(mol)
    mol.SetProp("_Name", pid)
    mol.SetProp("Compound_ID", pid)
    mol.SetProp("SMILES", smi)
    mol.SetProp("MW", f"{Descriptors.MolWt(mol):.2f}")
    mol.SetProp("cLogP", f"{Descriptors.MolLogP(mol):.2f}")
    mol.SetProp("HBD", str(Descriptors.NumHDonors(mol)))
    mol.SetProp("HBA", str(Descriptors.NumHAcceptors(mol)))
    mol.SetProp("RotB", str(Descriptors.NumRotatableBonds(mol)))
    mol.SetProp("Design_Rationale", rationale)
    mol.SetProp("Target", "P841")
    mol.SetProp("Design_Group", pid[0])
    mol.SetProp("Filter_Status", "PAINS_clean_Brenk_clean_NIH_clean")
    writer.write(mol)
writer.close()

# Verify
suppl = Chem.SDMolSupplier(out_path)
mols = [m for m in suppl if m]
print(f"SDF OK: {len(mols)} molecules")
print(f"Size: {os.path.getsize(out_path)} bytes")
print(f"IDs: {[m.GetProp('Compound_ID') for m in mols]}")
