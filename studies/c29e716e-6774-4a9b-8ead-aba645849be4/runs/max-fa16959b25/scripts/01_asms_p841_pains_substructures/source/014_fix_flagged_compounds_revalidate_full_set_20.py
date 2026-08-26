
# Fix flagged compounds and revalidate full set of 20
proposals_v2 = [
    # Group A: R1 bioisosteres, best R2 pyrrole-benzyl
    ("A1", "O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2",
     "Best R2 + 4-fluorophenyl R1. Replaces fluoroalkoxy-pyridine with simpler 4-F-phenyl. Tests whether pyridine N in R1 is needed or aryl-F alone sufficient. MW ~455, clean."),
    ("A2", "O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1cnc(OC(F)(F)F)cc1)CC2",
     "Best R2 + trifluoromethoxy-pyridine R1. OCF3 bioisostere of OCH2CF3 — shorter chain, same acceptor, better metabolic stability. Validated clean."),
    ("A3", "O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(C(F)(F)F)nc1)CC2",
     "Best R2 + 4-CF3-pyridine-2-carbonyl R1. Tests CF3 vs ether for lipophilic pocket engagement on R1 side. Clean compound."),

    # Group B: Replace aniline PAINS — use non-aniline heteroaromatic R2
    ("B1", "Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccncc4)nc3C2)oc2ccccc12",
     "EDS00480994 analogue: swap 4-(N-methylpiperazino)aniline for 4-pyridylmethyl. Removes aniline PAINS entirely. Keeps benzofuran R1. MW 426, clean."),
    ("B2", "Cc1c(C(=O)N2CCc3ccc(C(=O)NCC4CCOCC4)nc3C2)oc2ccccc12",
     "EDS00480994 analogue: replace aniline-piperazine R2 with tetrahydropyranyl-methyl. Non-aniline aliphatic R2 — tests if HBA from O-ring maintains activity without PAINS amine."),
    ("B3", "Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccc(F)cc4)nc3C2)oc2ccccc12",
     "EDS00480994 analogue: minimal clean R2 = 4-fluorobenzyl. Benchmark to see if basic nitrogen in R2 is essential, or fluorobenzyl alone engages pocket. MW 458, clean."),

    # Group C: Best R1 + clean R2 variants
    ("C1", "O=C(NCc1ccc(N2CCOCC2)nc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 5-(morpholino)pyridin-2-yl-methyl R2. Moves morpholine to pyridine ring (not aniline context). Combines best R1 with HBA-rich non-aniline R2. Clean."),
    ("C2", "O=C(NCc1cccc(F)c1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 3-fluorobenzyl. Minimal R2 test — probes whether F on benzyl adds directed binding vs unsubstituted (EDS00490706 rank 468 had plain benzyl). MW 487."),
    ("C3", "O=C(NCc1cnc(C)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 5-methylpyridin-2-ylmethyl R2. Clean heteroaromatic R2, bioisostere of methylpyrimidine from cleanest active EDS00444974. Tests optimal N count in R2 heterocycle."),
    ("C4", "O=C(NCc1ccc(-n2ccnc2)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 4-(imidazol-1-yl)benzyl R2. Tests N-linked heterocycle on benzyl vs alkyl-amino; imidazole adds HBA without aniline context. Clean."),

    # Group D: 4,4-difluorocyclohexyl R2 with upgraded R1
    ("D1", "O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 4,4-difluorocyclohexylamine R2. Direct combination of two validated structural elements from different actives. EDS00469766 showed aliphatic R2 works; upgrade its R1."),
    ("D2", "O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2",
     "4,4-difluorocyclohexyl R2 + 4-fluorophenyl R1. Lower MW (~418), all-fluorine compound, no flags. Test minimum pharmacophore with fluorine-rich core."),

    # Group E: Simplified / lower MW
    ("E1", "Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2ccc(F)cc2)CC3)cn1",
     "EDS00444974-type methylpyrimidine R2 + 4-fluorophenyl R1. Lowest MW clean active template. MW 406. Tests fluorophenyl vs isobutyryl on smallest scaffold."),
    ("E2", "Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2ccc(OCC(F)(F)F)nc2)CC3)cn1",
     "Best R1 + EDS00444974 methylpyrimidine R2. Direct upgrade of cleanest active with highest-potency R1. Priority compound — tests if lack of R1 limited EDS00444974 activity."),
    ("E3", "Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)C4(F)CC4)CC3)cn1",
     "EDS00444974-type R2 + 1-fluorocyclopropane carbonyl R1. Smallest possible R1, rigid, one F for polarity. MW 381, clean. Tests minimal R1 sufficient for binding."),

    # Group F: Novel / linker exploration
    ("F1", "O=C(NCC1(c2ccccc2)CCOCC1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + spirocyclic-benzyl-THF R2 from EDS00470458. That compound had weak AS (0.0015) with suboptimal R1. Tests if poor R1 explained weak hit."),
    ("F2", "O=C(NCc1ccsc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + thienylmethyl R2 from EDS00474254. EDS00474254 had R2 interest but weak R1. Minimal, clean, MW 476. Thienyl provides HBA sulfur and aromatic contact."),
    ("F3", "O=C(NCc1cc(F)ccc1F)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 2,4-difluorobenzyl R2. Removes Cl from EDS00459274 (Brenk:halogenated_ring), keeps two F atoms. Derisked analogue of rank-314 hit with best R1."),
    ("F4", "O=C(NCc1ccc(S(C)(=O)=O)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + methylsulfonyl-benzyl R2 from EDS00474362. Sulfonyl = HBA, no basicity, good solubility. Direct R1 upgrade of rank-794 hit."),
    ("F5", "O=C(NCc1cccc(N2CCOCC2)n1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2",
     "Best R1 + 2-(morpholino)pyridyl-methyl R2 from EDS00459346. EDS00459346 (rank 294) had dimethylpyrazole R1; upgrade to best R1. Morpholine-pyridyl R2 — no aniline, HBA."),
]

print(f"{'ID':<4} {'Valid':<6} {'MW':>6} {'LogP':>6} {'HBD':>4} {'RotB':>5}  Flags")
print("-"*85)
clean_count = 0
for pid, smi, rationale in proposals_v2:
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        print(f"{pid:<4} INVALID  {smi[:50]}")
        continue
    mw = Descriptors.MolWt(mol)
    lp = Descriptors.MolLogP(mol)
    hbd = Descriptors.NumHDonors(mol)
    rotb = Descriptors.NumRotatableBonds(mol)
    pains_hit = pains_catalog.GetFirstMatch(mol)
    brenk_hit = brenk_catalog.GetFirstMatch(mol)
    flags = []
    if pains_hit: flags.append(f"PAINS:{pains_hit.GetDescription()}")
    if brenk_hit: flags.append(f"Brenk:{brenk_hit.GetDescription()}")
    flag_str = '; '.join(flags) if flags else 'clean'
    if not flags: clean_count += 1
    print(f"{pid:<4} OK      {mw:>6.0f} {lp:>6.2f} {hbd:>4} {rotb:>5}  {flag_str}")

print(f"\nClean compounds: {clean_count}/20")
