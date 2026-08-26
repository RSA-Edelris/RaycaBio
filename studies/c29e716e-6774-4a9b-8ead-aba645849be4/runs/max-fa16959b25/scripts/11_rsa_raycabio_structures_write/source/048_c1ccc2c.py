
from rdkit.Chem import SDWriter, AllChem
import os

proposals_v2 = [
    ("A1", "O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2",
     "Best R2 (2-pyrrolyl-benzyl) + 4-fluorophenyl R1. Tests aryl-F sufficient for R1 pocket vs pyridine-ether."),
    ("A2", "O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1cnc(OC(F)(F)F)cc1)CC2",
     "Best R2 + OCF3-pyridine R1. Bioisostere of top hit trifluoroethoxy — shorter chain, better metabolic stability."),
    ("A3", "O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(C(F)(F)F)nc1)CC2",
     "Best R2 + 4-CF3-pyridine-2-carbonyl R1. CF3 vs ether for lipophilic R1 pocket."),
    ("B1", "Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccncc4)nc3C2)oc2ccccc12",
     "EDS00480994 PAINS-free analogue: 4-pyridylmethyl replaces piperazino-aniline. Removes anil_di_alk_E flag."),
    ("B2", "Cc1c(C(=O)N2CCc3ccc(C(=O)NCC4CCOCC4)nc3C2)oc2ccccc12",
     "EDS00480994 analogue: tetrahydropyranyl-methyl R2, no amine. Tests if basic N essential."),
    ("B3", "Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccc(F)cc4)nc3C2)oc2ccccc12",
     "EDS00480994 analogue: 4-fluorobenzyl R2. Minimal clean benchmark for piperazine contribution."),
    ("C1", "O=C(NCc1ccc(N2CCOCC2)nc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 5-(morpholino)pyridin-2-ylmethyl R2. Basic N on pyridine, no aniline context, clean."),
    ("C2", "O=C(NCc1cccc(F)c1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 3-fluorobenzyl R2. Minimal R2 probe — confirms R1 primacy hypothesis."),
    ("C3", "O=C(NCc1cnc(C)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 5-methylpyridinylmethyl R2. Mono-aza bioisostere of methylpyrimidine R2."),
    ("C4", "O=C(NCc1ccc(-n2ccnc2)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 4-(imidazol-1-yl)benzyl R2. N-heterocycle on benzyl, HBA imidazole, no aniline."),
    ("D1", "O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 4,4-difluorocyclohexylamine R2. Combines top-hit R1 with EDS00469766 R2. Priority compound."),
    ("D2", "O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2",
     "4,4-difluorocyclohexyl R2 + 4-fluorophenyl R1. MW 417, most constrained, LE probe."),
    ("E1", "Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2ccc(F)cc2)CC3)cn1",
     "EDS00444974 R2 (methylpyrimidine) + 4-fluorophenyl R1. Rigid fluorophenyl upgrade of cleanest active."),
    ("E2", "Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2ccc(OCC(F)(F)F)nc2)CC3)cn1",
     "EDS00444974 R2 + best R1. Top priority: direct upgrade of cleanest active. LogP 2.64, no flags."),
    ("E3", "Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)C4(F)CC4)CC3)cn1",
     "EDS00444974 R2 + 1-fluorocyclopropyl R1. MW 369, most rigid, metabolic stability probe."),
    ("F1", "O=C(NCC1(c2ccccc2)CCOCC1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + spirocyclic-benzyl-THF R2 (EDS00470458 rescue). Tests if poor R1 explained weak AS=0.0015."),
    ("F2", "O=C(NCc1ccsc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + thienylmethyl R2 (EDS00474254 upgrade). Compact, aromatic S contact."),
    ("F3", "O=C(NCc1cc(F)ccc1F)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 2,4-difluorobenzyl R2. Derisked analogue of Brenk EDS00459274 (Cl removed)."),
    ("F4", "O=C(NCc1ccc(S(C)(=O)=O)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + methylsulfonyl-benzyl R2 (EDS00474362 upgrade). HBA sulfonyl, no basicity."),
    ("F5", "O=C(NCc1cccc(N2CCOCC2)n1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + morpholino-pyridylmethyl R2. R1 swap on EDS00459346 rank-294 clean hit."),
]

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
size = os.path.getsize(out_path)
print(f"Written: {out_path} ({size} bytes, 20 molecules)")
