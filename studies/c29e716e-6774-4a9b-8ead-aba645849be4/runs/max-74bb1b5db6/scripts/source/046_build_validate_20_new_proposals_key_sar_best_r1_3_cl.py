
# Build & validate 20 new proposals
# Key SAR:
# Best R1: 3-Cl-benzothiophen-2-carbonyl (r1a) AND 3-MeBFO (r1b)
# Best clean R2: 4-pyridylbenzyl (r2a); 3-Cl-BTP+pyridylbenzyl NEVER MADE
# PAINS flag ubiquitous but NOT driving potency (pIC50 lower in PAINS vs clean top)
# LogP positively correlated (r=0.23); biaryl R2 >> simple benzyl or heteroaryl-methyl

proposals = [
    # --- Group A: Critical untested combos (best R1 × clean R2) ---
    ("A1", "O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2",
     "3-Cl-BTP R1 + 4-pyridylbenzyl R2 (naphthyridine). THE critical missing combination. Best R1 (5.959) + best clean R2 (5.955) never made together. Predicted pIC50 ≥6.3 by independent additivity of both elements."),
    ("A2", "O=C(NCc1ccc(-c2ccncc2)cc1)c1cc2c(s1)CCN(C(=O)c1sc3ccccc3c1Cl)C2",
     "3-Cl-BTP R1 + 4-pyridylbenzyl R2 (thienopyridine core). Tests if the ring-sulfur in the core amplifies 3-Cl-BTP R1 synergy, as CTX-1020670 shows thienopyridine+3-Cl-BTP = 5.903 even with simple benzyl."),
    ("A3", "O=C(NCc1ccc(C2CCOCC2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2",
     "3-Cl-BTP R1 + THP-benzyl R2. CTX-1020696 proved THP-benzyl is second-best R2 with 3-MeBFO (5.879). Upgrading to best R1 tests additive contribution."),
    ("A4", "O=C(NCc1ccc2c(c1)NCCC2)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2",
     "3-Cl-BTP R1 + 1,2,3,4-tetrahydroisoquinolinyl R2 (naphthyridine). CTX-1020695 showed tetrahydroisoquinolinyl = 5.565 with 3-MeBFO. Rigid bicyclic R2 preorganises binding, predicted improvement with best R1."),

    # --- Group B: Extend R2 biaryl (add HBA to terminal heterocycle) ---
    ("B1", "O=C(NCc1ccc(-c2ncccn2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2",
     "3-Cl-BTP R1 + 4-(pyrimidin-2-yl)benzyl R2. Extra N in pyrimidinyl adds a second HBA face. If the binding pocket has a H-bond donor that the pyridine N barely reaches, pyrimidine 2-N could capture it."),
    ("B2", "O=C(NCc1ccc(-c2ccnc(N)c2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2",
     "3-Cl-BTP R1 + 4-(2-aminopyridin-4-yl)benzyl. Adds HBD (NH2) to the terminal pyridyl. If the pocket has a carbonyl or HBA residue adjacent to the pyridyl site, the NH2 captures it. Introduces one HBD = up to 1.5 log unit gain."),
    ("B3", "O=C(NCc1ccc(-c2ccnc(C)c2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2",
     "3-Cl-BTP R1 + 4-(2-methylpyridin-4-yl)benzyl. 2-methyl on pyridine blocks 2-H (metabolic site) and modulates electronics. Tests whether steric/electronic change on pyridine N-neighbour improves or worsens binding."),
    ("B4", "O=C(NCc1ccc(-c2cc(-c3ccncc3)cc(-c3ccncc3)c2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2",
     "3-Cl-BTP R1 + 3,5-di(pyridin-4-yl)benzyl. Two pyridyl groups symmetrically placed. Explores whether two HBA contacts from the R2 chain further improve potency. MW ~600, but tests the concept."),

    # --- Group C: R1 modifications, keeping pyridylbenzyl R2 ---
    ("C1", "O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1C(F)(F)F)CC2",
     "3-CF3-BTP R1 + pyridylbenzyl R2. CF3 is electron-withdrawing like Cl but more lipophilic, occupies same volume. Tests halogen vs perfluoroalkyl at R1 C3, exploring deeper pocket lipophilic contacts."),
    ("C2", "O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3cc(F)ccc3c1Cl)CC2",
     "5-F-3-Cl-BTP R1 + pyridylbenzyl R2. F at position 5 of the benzo ring blocks metabolic hydroxylation. SAR probe for R1 benzo-ring tolerance and metabolic stability improvement. Dual fluorine effect."),
    ("C3", "O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1c(C)oc3cc(F)ccc13)CC2",
     "5-F-3-MeBFO R1 + pyridylbenzyl R2. F at C5 of benzofuran ring adds electron-withdrawal, metabolic blocking, and a weak C-H...F interaction. Tests benzofuran ring substitution tolerance."),
    ("C4", "O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1cnn3ccncc13)CC2",
     "Pyrazolo[1,5-a]pyrimidine-2-carbonyl R1 + pyridylbenzyl R2. CTX-1020671 proved this R1 is active (5.463) with simple benzyl. Replacing benzyl with pyridylbenzyl should add ~0.47 units (from the CTX-1019471 vs CTX-1020698 delta). Bicyclic N-rich R1 may make additional hinge contacts."),
    ("C5", "O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1c(Cl)c3ccccc3n1C)CC2",
     "3-Cl-1-methylbenzimidazol-2-yl R1 + pyridylbenzyl R2. CTX-1020748 had this R1 (pIC50 5.556) with piperazino-aniline PAINS R2. Replacing PAINS R2 with clean pyridylbenzyl, expected improvement of ~0.4 units to ~5.9–6.0."),

    # --- Group D: Fluorine scan on the benzyl linker / pyridyl ring ---
    ("D1", "O=C(NCc1c(F)ccc(-c2ccncc2)c1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2",
     "3-Cl-BTP R1 + ortho-F-4-pyridylbenzyl R2. F at 2-position of the benzyl ring (ortho to CH2) can orient the amide via C-H...F electrostatic effect, potentially preorganising the R2 arm into the optimal binding geometry."),
    ("D2", "O=C(NCc1ccc(-c2ccncc2)cc1F)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2",
     "3-Cl-BTP R1 + 4-pyridyl-2-fluorobenzyl (F ortho to pyridyl on benzyl ring). F adjacent to the biaryl bond modulates torsional angle between rings, potentially locking the pyridyl into the binding-competent conformation."),
    ("D3", "O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3c(F)cccc3c1Cl)CC2",
     "3-Cl-4-F-BTP R1 (F on benzo ring) + pyridylbenzyl R2. F adjacent to the C3-Cl on benzothiophene tests whether the Cl activity comes from shape or electronics. F is smaller; replacing H with F at C4-benzo could add binding contacts."),

    # --- Group E: Novel R2 pharmacophores for additional HBA/HBD contacts ---
    ("E1", "O=C(NCc1ccc(-c2ccc(-c3ccncc3)cc2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2",
     "3-Cl-BTP R1 + 4-[4-(pyridin-4-yl)phenyl]benzyl (terphenyl-CH2). Extends the biaryl chain by one phenyl ring to reach deeper into a potential hydrophobic channel. Tests whether aromatic depth beyond biphenyl is tolerated or penalised."),
    ("E2", "O=C(NCc1ccc(-c2cccc3[nH]ccc23)cc1)c1ccc2c(n1)CN(C(=O)c1c(C)oc3ccccc13)CC2",
     "3-MeBFO R1 + 4-(1H-indol-4-yl)benzyl. Indole at R2 provides both HBD (NH) and a bicyclic aromatic face for stacking. Tests whether the R2 terminal heterocycle with a donor NH improves over the pyridyl acceptor."),
    ("E3", "O=C(NCc1ccc(-c2sc3ccccc3c2Cl)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2",
     "3-Cl-BTP R1 + 4-(3-Cl-benzo[b]thiophen-2-yl)benzyl (symmetrical bis-BTP). Mirrors the successful R1 at the R2 position. Creates a pseudo-symmetric molecule where both arms present similar halogenated aromatic surfaces — tests bimodal BTP engagement."),
    ("E4", "O=C(NCc1ccc(-c2ccncc2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccc(F)cc3c1Cl)CC2",
     "3-Cl-4-F-phenyl-BTP R1 + pyridylbenzyl R2. F at 5-position of BTP benzene ring (para to sulfur). Tests fluorine on the distal ring of R1 for improved contacts in an adjacent sub-pocket, similar to strategy in clinical compounds."),
]

print(f"{'ID':<4} {'Valid':<6} {'MW':>6} {'LogP':>6} {'HBD':>4} {'RotB':>5}  Flags")
print("-"*85)
clean_cnt = 0
for pid, smi, _ in proposals:
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        print(f"{pid:<4} INVALID  {smi[:60]}")
        continue
    mw   = Descriptors.MolWt(mol)
    lp   = Descriptors.MolLogP(mol)
    hbd  = Descriptors.NumHDonors(mol)
    rotb = Descriptors.NumRotatableBonds(mol)
    p    = pains_cat.GetFirstMatch(mol)
    b    = brenk_cat.GetFirstMatch(mol)
    flags = []
    if p: flags.append(f"PAINS:{p.GetDescription()}")
    if b: flags.append(f"Brenk:{b.GetDescription()}")
    fstr = '; '.join(flags) if flags else 'clean'
    if not flags: clean_cnt += 1
    print(f"{pid:<4} OK      {mw:>6.0f} {lp:>6.2f} {hbd:>4} {rotb:>5}  {fstr}")

print(f"\nClean: {clean_cnt}/20")
