
from rdkit.Chem import SDWriter, AllChem
import os

proposals_v2 = [
    ("A1", "O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2",
     "Best R2 + 4-fluorophenyl R1. Tests whether pyridine N in R1 is needed or aryl-F alone sufficient."),
    ("A2", "O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1cnc(OC(F)(F)F)cc1)CC2",
     "Best R2 + OCF3-pyridine R1. Bioisostere of OCH2CF3 in top hit, better metabolic stability."),
    ("A3", "O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(C(F)(F)F)nc1)CC2",
     "Best R2 + 4-CF3-pyridine-2-carbonyl R1. Tests CF3 vs ether for lipophilic pocket engagement."),
    ("B1", "Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccncc4)nc3C2)oc2ccccc12",
     "EDS00480994 PAINS-free analogue: 4-pyridylmethyl R2 replaces dialkyl-aniline. Removes anil_di_alk_E flag."),
    ("B2", "Cc1c(C(=O)N2CCc3ccc(C(=O)NCC4CCOCC4)nc3C2)oc2ccccc12",
     "EDS00480994 analogue: tetrahydropyranyl-methyl R2. Non-aniline aliphatic HBA probe."),
    ("B3", "Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccc(F)cc4)nc3C2)oc2ccccc12",
     "EDS00480994 analogue: 4-fluorobenzyl R2. Minimal control, no basic N, tests R2 basicity requirement."),
    ("C1", "O=C(NCc1ccc(N2CCOCC2)nc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 5-(morpholino)pyridin-2-yl-methyl R2. Clean HBA-rich non-aniline basic motif."),
    ("C2", "O=C(NCc1cccc(F)c1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 3-fluorobenzyl R2. Minimal probe of R1 primacy; upgrade of EDS00490706 (rank 468)."),
    ("C3", "O=C(NCc1cnc(C)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 5-methylpyridin-2-ylmethyl R2. Bioisostere of methylpyrimidine from EDS00444974."),
    ("C4", "O=C(NCc1ccc(-n2ccnc2)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 4-(imidazol-1-yl)benzyl R2. N-linked heterocycle avoids aniline context."),
    ("D1", "O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "PRIORITY. Best R1 + 4,4-difluorocyclohexylamine R2. Combines two strongest structural elements from separate actives."),
    ("D2", "O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2",
     "4,4-difluorocyclohexyl R2 + 4-fluorophenyl R1. Lowest MW (417), highest ligand efficiency target."),
    ("E1", "Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2ccc(F)cc2)CC3)cn1",
     "EDS00444974 scaffold + 4-fluorophenyl R1. Tests isobutyryl vs fluorophenyl on cleanest active template."),
    ("E2", "Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2ccc(OCC(F)(F)F)nc2)CC3)cn1",
     "PRIORITY. EDS00444974 R2 + best R1. Direct upgrade of cleanest active. Best drug-likeness (LogP 2.64)."),
    ("E3", "Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)C4(F)CC4)CC3)cn1",
     "EDS00444974 R2 + 1-fluorocyclopropane-carbonyl R1. Lowest MW (369), conformational lock, metabolic stability."),
    ("F1", "O=C(NCC1(c2ccccc2)CCOCC1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + spirocyclic benzyl-THF R2 from EDS00470458. Tests if weak hit was limited by R1."),
    ("F2", "O=C(NCc1ccsc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + thienylmethyl R2 from EDS00474254. Clean compact R2, aromatic sulfur HBA contact."),
    ("F3", "O=C(NCc1cc(F)ccc1F)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Derisked EDS00459274: removes aryl-Cl (Brenk), retains 2,4-di-F, adds best R1."),
    ("F4", "O=C(NCc1ccc(S(C)(=O)=O)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + methylsulfonyl-benzyl R2 from EDS00474362. HBA sulfonyl, no basicity, good solubility."),
    ("F5", "O=C(NCc1cccc(N2CCOCC2)n1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "PRIORITY. Best R1 + morpholino-pyridyl-methyl R2 from EDS00459346 (rank 294). Direct R1 upgrade."),
]

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
