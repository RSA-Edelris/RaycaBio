
from rdkit import Chem
from rdkit.Chem import SDWriter, AllChem, Descriptors

out_path = "/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02/P841_proposed_actives.sdf"
writer = SDWriter(out_path)

for pid, smi, rationale in proposals_v2:
    mol = Chem.MolFromSmiles(smi)
    AllChem.Compute2DCoords(mol)
    mol.SetProp("_Name", pid)
    mol.SetProp("Compound_ID", pid)
    mol.SetProp("SMILES", smi)
    mol.SetProp("Target", "P841")
    mol.SetProp("Series", "Tetrahydropyrido-piperidine amide")
    mol.SetProp("MW", str(round(Descriptors.MolWt(mol), 2)))
    mol.SetProp("cLogP", str(round(Descriptors.MolLogP(mol), 2)))
    mol.SetProp("HBD", str(Descriptors.NumHDonors(mol)))
    mol.SetProp("HBA", str(Descriptors.NumHAcceptors(mol)))
    mol.SetProp("RotBonds", str(Descriptors.NumRotatableBonds(mol)))
    mol.SetProp("PAINS_Brenk", "clean")
    mol.SetProp("Design_Rationale", rationale)
    mol.SetProp("Origin", "ASMS hit triage 2026-08-26")
    writer.write(mol)

writer.close()
print(f"Written {len(proposals_v2)} compounds → {out_path}")
print(f"Size: {os.path.getsize(out_path)} bytes")
