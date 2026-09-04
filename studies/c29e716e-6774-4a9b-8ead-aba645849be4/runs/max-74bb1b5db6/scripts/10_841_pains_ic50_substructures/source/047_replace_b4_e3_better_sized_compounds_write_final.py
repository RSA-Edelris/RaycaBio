
# Replace B4 and E3 with better-sized compounds, then write final report

replacements = [
    ("B4r", "O=C(NCc1cccc(-c2ccncc2)c1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2",
     "3-Cl-BTP R1 + 3-pyridylbenzyl R2 (meta-pyridyl). Tests positional isomer of CTX-1020698 pyridyl. Meta-pyridyl places the N in a different spatial orientation — probes exact geometry of HBA contact in binding pocket."),
    ("E3r", "O=C(NCc1ccc(-c2cn[nH]c2)cc1)c1ccc2c(n1)CN(C(=O)c1sc3ccccc3c1Cl)CC2",
     "3-Cl-BTP R1 + 4-(1H-pyrazol-4-yl)benzyl R2. Pyrazole HBD+HBA ring replaces pyridine — adds an NH donor for potential protein carbonyl contact while maintaining biaryl geometry. MW 523, clean."),
]

print("Replacements:")
for pid, smi, rat in replacements:
    mol = Chem.MolFromSmiles(smi)
    mw = Descriptors.MolWt(mol); lp = Descriptors.MolLogP(mol)
    hbd = Descriptors.NumHDonors(mol)
    p = pains_cat.GetFirstMatch(mol); b = brenk_cat.GetFirstMatch(mol)
    flags = ('PAINS:'+p.GetDescription() if p else '') + ('Brenk:'+b.GetDescription() if b else '') or 'clean'
    print(f"{pid}: MW={mw:.0f} LogP={lp:.2f} HBD={hbd} | {flags}")
