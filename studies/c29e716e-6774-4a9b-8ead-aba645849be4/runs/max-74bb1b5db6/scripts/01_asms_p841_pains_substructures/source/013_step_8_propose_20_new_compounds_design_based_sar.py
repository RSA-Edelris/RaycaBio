
# Step 8: Propose 20 new compounds — design based on SAR
# Core scaffold: O=C(NCC-R2)c1ccc2c(n1)CN(C(=O)-R1)CC2
# Best R1: c1ccc(OCC(F)(F)F)nc1 (4-trifluoroethoxypyridine)
# Good R2: Cc1cnc(C)nc1 (methylpyrimidine), 4,4-difluorocyclohexyl, benzyl-pyrrole

# Define 20 new SMILES (core + R-group combinations)
proposals = [
    # --- Group A: Vary R1 fluoropyridine/fluorine bioisosteres, keep pyrrole-benzyl R2 ---
    ("A1", "O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(F)nc1)CC2",
     "Best R2 (2-pyrrolyl-benzyl). R1 changed to 4-fluoropyridine-2-carbonyl — simpler, lower MW, removes fluoroalkyl chain. Tests whether C-F on pyridine sufficient vs ether."),
    ("A2", "O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1cnc(OC(F)(F)F)cc1)CC2",
     "R1 = 4-(trifluoromethoxy)pyridine — bioisostere of trifluoroethoxy, fewer carbons, better metabolic stability. Same R2."),
    ("A3", "O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(C(F)(F)F)nc1)CC2",
     "R1 = 4-(trifluoromethyl)pyridine-2-carbonyl — CF3 instead of OCH2CF3. Tests direct lipophilic CF3 vs ether."),

    # --- Group B: Replace PAINS aniline R2 with clean analogues ---
    ("B1", "Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccncc4)nc3C2)oc2ccccc12",
     "EDS00480994 analogue: replace PAINS 4-(N-methylpiperazino)aniline-benzyl with 4-pyridyl-methyl. Removes aniline PAINS flag. Keeps benzofuran R1."),
    ("B2", "Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccc(N5CCOCC5)cc4)nc3C2)oc2ccccc12",
     "EDS00480994 analogue: replace N-methylpiperazine with morpholine — removes basic nitrogen that can cause PAINS aniline context, improves aqueous solubility, lower cLogP."),
    ("B3", "Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccc(N5CCC(F)(F)C5)cc4)nc3C2)oc2ccccc12",
     "EDS00480994 analogue: replace piperazine with 3,3-difluoropyrrolidine — removes basic piperazine, introduces H-bond acceptor F atoms, modulates lipophilicity."),

    # --- Group C: Best R1 (trifluoroethoxypyridine) with unexplored clean R2s ---
    ("C1", "O=C(NCc1ccc(N2CCOCC2)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + morpholine-para-benzyl R2. Morpholine bioisostere of piperazine, lower basicity, better ADMET. Direct combination of best-observed R1 with clean basic motif."),
    ("C2", "O=C(NCc1cccc(F)c1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 3-fluorobenzyl R2 (minimal, from EDS00490706 benzyl with added F). Tests if fluorine on benzyl improves binding vs unsubstituted. MW reduced."),
    ("C3", "O=C(NCc1cnc(C)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 5-methylpyridin-2-yl-methyl R2. Replaces pyrimidine of EDS00444974 R2 with pyridine. Tests optimal heteroaromatic on R2 side. Clean compound."),
    ("C4", "O=C(NCc1ccc(-n2ccnc2)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 4-(1H-imidazol-1-yl)benzyl R2. Tests imidazole-benzyl motif: HBA nitrogen, lower MW vs piperazine-benzyl."),

    # --- Group D: Combine best R1 with 4,4-difluorocyclohexyl R2 (EDS00469766 series) ---
    ("D1", "O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 (trifluoroethoxypyridyl) + 4,4-difluorocyclohexyl amine R2 from EDS00469766. Direct combination of two validated substitution patterns. MW manageable at ~481 Da."),
    ("D2", "O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1cnc(F)cc1)CC2",
     "4,4-difluorocyclohexyl R2 + fluoropyridine R1. Simpler analogue of D1, lower MW (~415 Da). All-fluorine compound: good for metabolic stability and selectivity."),

    # --- Group E: Scaffold simplification / lower MW ---
    ("E1", "Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2ccc(F)nc2)CC3)cn1",
     "EDS00444974-type (cleanest active): keep methylpyrimidine R2, replace isobutyryl R1 with 4-fluoropyridyl. Tests if H-bond network of pyrimidine-methyl R2 tolerates heteroaromatic R1."),
    ("E2", "Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2ccc(OCC(F)(F)F)nc2)CC3)cn1",
     "EDS00444974-type R2 (methylpyrimidine) + best R1 (trifluoroethoxypyridyl). Direct upgrade of the cleanest active with the best R1. MW ~490 Da, no flags."),
    ("E3", "Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)C3(F)CC3)CC2)cn1",
     "EDS00444974-type: R2=methylpyrimidine, R1=1-fluorocyclopropane-carbonyl. Very small R1, rigid cyclopropyl, F adds polarity. Low MW (~380 Da). Tests minimal R1 requirement."),

    # --- Group F: Novel scaffolds / linker exploration ---
    ("F1", "O=C(NCC1(c2ccccc2)CCOCC1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "EDS00470458 spirobenzyl-THF R2 + best R1. EDS00470458 had weak AS=0.0015; combining its R2 with best R1 tests if the spirocyclic R2 is tolerated with strong R1."),
    ("F2", "O=C(NCc1ccsc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "EDS00474254-derived: thienyl-methyl R2 + best R1. EDS00474254 had thienyl methyl R2; upgrade R1 to best. MW ~443 Da, no flags, excellent drug-likeness."),
    ("F3", "O=C(NCc1c(F)ccc(F)c1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "EDS00459274-type: remove chlorine (Brenk halogenated ring), keep two fluorines + best R1. Clean analogue of Brenk-flagged EDS00459274."),
    ("F4", "O=C(NCc1ccc(S(C)(=O)=O)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "EDS00474362-derived: methylsulfonyl-benzyl R2 + best R1. Sulfonyl adds H-bond acceptors without basicity. Upgrade a weak hit (AS=0.0026) with best R1."),
    ("F5", "O=C(NCc1cccc(N2CCOCC2)n1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + morpholine-pyridyl-methyl R2 (from EDS00459346 which had morpholine pyridyl). Replaces EDS00459346 weak R1 (dimethylpyrazole) with best R1. Direct improvement of rank-294 hit."),
]

# Validate all SMILES
print(f"{'ID':<4} {'Valid':<6} {'MW':>6} {'LogP':>6} {'Flags'}")
print("-"*80)
flagged = []
from rdkit.Chem.MolStandardize import rdMolStandardize
te = rdMolStandardize.TautomerEnumerator()

for pid, smi, rationale in proposals:
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        print(f"{pid:<4} INVALID  --- SMILES: {smi[:60]}")
        continue
    mw = Descriptors.MolWt(mol)
    lp = Descriptors.MolLogP(mol)
    # Check PAINS
    pains_hit = pains_catalog.GetFirstMatch(mol)
    brenk_hit = brenk_catalog.GetFirstMatch(mol)
    flags = []
    if pains_hit: flags.append(f"PAINS:{pains_hit.GetDescription()}")
    if brenk_hit: flags.append(f"Brenk:{brenk_hit.GetDescription()}")
    flag_str = '; '.join(flags) if flags else 'clean'
    print(f"{pid:<4} OK      {mw:>6.0f} {lp:>6.2f}  {flag_str}")
