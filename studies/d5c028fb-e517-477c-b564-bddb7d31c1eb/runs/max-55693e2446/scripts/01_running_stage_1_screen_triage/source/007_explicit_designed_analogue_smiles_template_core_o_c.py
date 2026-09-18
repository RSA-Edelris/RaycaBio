
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors

# -----------------------------------------------------------------------
# Explicit designed analogue SMILES
# Template core: O=C(R1)N1Cc2nc(C(=O)NCC_R2)ccc2CC1
# Ring 1 = piperidine ring, ring 2 = pyridine ring of THN core
# R1 uses ring numbers 3[+], R2 uses ring numbers 5[+]
# -----------------------------------------------------------------------

designed = [
    # ------- A-series: Best R1 (2-OCH2CF3-pyridin-5-yl) × varied R2 -------
    ("A01","R1=2-CF3EtO-py5, R2=2-pyrrolyl-Bn",
     "O=C(c3cnc(OCC(F)(F)F)cc3)N1Cc2nc(C(=O)NCc4ccccc4-n5cccc5)ccc2CC1"),
    ("A02","R1=2-CF3EtO-py5, R2=4-piperazino-Bn",
     "O=C(c3cnc(OCC(F)(F)F)cc3)N1Cc2nc(C(=O)NCc4ccc(N5CCNCC5)cc4)ccc2CC1"),
    ("A03","R1=2-CF3EtO-py5, R2=4-NMePiperazino-Bn",
     "O=C(c3cnc(OCC(F)(F)F)cc3)N1Cc2nc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)ccc2CC1"),
    ("A04","R1=2-CF3EtO-py5, R2=4-morpholino-Bn",
     "O=C(c3cnc(OCC(F)(F)F)cc3)N1Cc2nc(C(=O)NCc4ccc(N5CCOCC5)cc4)ccc2CC1"),
    ("A05","R1=2-CF3EtO-py5, R2=pyrimidin-5-ylmethyl",
     "O=C(c3cnc(OCC(F)(F)F)cc3)N1Cc2nc(C(=O)NCc4cnccn4)ccc2CC1"),
    ("A06","R1=2-CF3EtO-py5, R2=pyridin-4-ylmethyl",
     "O=C(c3cnc(OCC(F)(F)F)cc3)N1Cc2nc(C(=O)NCc4ccncc4)ccc2CC1"),
    ("A07","R1=2-CF3EtO-py5, R2=4-F-Bn",
     "O=C(c3cnc(OCC(F)(F)F)cc3)N1Cc2nc(C(=O)NCc4ccc(F)cc4)ccc2CC1"),
    ("A08","R1=2-CF3EtO-py5, R2=4-CF3-Bn",
     "O=C(c3cnc(OCC(F)(F)F)cc3)N1Cc2nc(C(=O)NCc4ccc(C(F)(F)F)cc4)ccc2CC1"),
    ("A09","R1=2-CF3EtO-py5, R2=4,4-diF-cyclohexyl",
     "O=C(c3cnc(OCC(F)(F)F)cc3)N1Cc2nc(C(=O)NC3CCC(F)(F)CC3)ccc2CC1"),
    # ------- B-series: Benzofuran R1 × varied R2 -------
    ("B01","R1=benzofuran-2-yl, R2=2-pyrrolyl-Bn",
     "O=C(c3cc4ccccc4o3)N1Cc2nc(C(=O)NCc4ccccc4-n5cccc5)ccc2CC1"),
    ("B02","R1=benzofuran-2-yl, R2=4-piperazino-Bn",
     "O=C(c3cc4ccccc4o3)N1Cc2nc(C(=O)NCc4ccc(N5CCNCC5)cc4)ccc2CC1"),
    ("B03","R1=benzofuran-2-yl, R2=4-morpholino-Bn",
     "O=C(c3cc4ccccc4o3)N1Cc2nc(C(=O)NCc4ccc(N5CCOCC5)cc4)ccc2CC1"),
    ("B04","R1=benzofuran-2-yl, R2=pyrimidin-5-ylmethyl",
     "O=C(c3cc4ccccc4o3)N1Cc2nc(C(=O)NCc4cnccn4)ccc2CC1"),
    ("B05","R1=benzofuran-2-yl, R2=4,4-diF-cyclohexyl",
     "O=C(c3cc4ccccc4o3)N1Cc2nc(C(=O)NC3CCC(F)(F)CC3)ccc2CC1"),
    # ------- C-series: Benzothiophene R1 × varied R2 -------
    ("C01","R1=benzothiophen-2-yl, R2=2-pyrrolyl-Bn",
     "O=C(c3cc4ccccc4s3)N1Cc2nc(C(=O)NCc4ccccc4-n5cccc5)ccc2CC1"),
    ("C02","R1=benzothiophen-2-yl, R2=4-piperazino-Bn",
     "O=C(c3cc4ccccc4s3)N1Cc2nc(C(=O)NCc4ccc(N5CCNCC5)cc4)ccc2CC1"),
    ("C03","R1=benzothiophen-2-yl, R2=4,4-diF-cyclohexyl",
     "O=C(c3cc4ccccc4s3)N1Cc2nc(C(=O)NC3CCC(F)(F)CC3)ccc2CC1"),
    # ------- D-series: CF3-pyridine R1 × varied R2 -------
    ("D01","R1=5-CF3-pyridin-3-yl, R2=2-pyrrolyl-Bn",
     "O=C(c3cncc(C(F)(F)F)c3)N1Cc2nc(C(=O)NCc4ccccc4-n5cccc5)ccc2CC1"),
    ("D02","R1=5-CF3-pyridin-3-yl, R2=4-piperazino-Bn",
     "O=C(c3cncc(C(F)(F)F)c3)N1Cc2nc(C(=O)NCc4ccc(N5CCNCC5)cc4)ccc2CC1"),
    ("D03","R1=5-CF3-pyridin-3-yl, R2=4,4-diF-cyclohexyl",
     "O=C(c3cncc(C(F)(F)F)c3)N1Cc2nc(C(=O)NC3CCC(F)(F)CC3)ccc2CC1"),
    # ------- E-series: 2-OMe-naphthyl R1 × varied R2 -------
    ("E01","R1=2-OMe-naphthyl, R2=2-pyrrolyl-Bn",
     "O=C(c3ccc4cc(OC)ccc4c3)N1Cc2nc(C(=O)NCc4ccccc4-n5cccc5)ccc2CC1"),
    ("E02","R1=2-OMe-naphthyl, R2=4-piperazino-Bn",
     "O=C(c3ccc4cc(OC)ccc4c3)N1Cc2nc(C(=O)NCc4ccc(N5CCNCC5)cc4)ccc2CC1"),
    ("E03","R1=2-OMe-naphthyl, R2=4,4-diF-cyclohexyl",
     "O=C(c3ccc4cc(OC)ccc4c3)N1Cc2nc(C(=O)NC3CCC(F)(F)CC3)ccc2CC1"),
    # ------- F-series: Quinoline R1 × varied R2 -------
    ("F01","R1=quinolin-3-yl, R2=2-pyrrolyl-Bn",
     "O=C(c3cnc4ccccc4c3)N1Cc2nc(C(=O)NCc4ccccc4-n5cccc5)ccc2CC1"),
    ("F02","R1=quinolin-3-yl, R2=4-piperazino-Bn",
     "O=C(c3cnc4ccccc4c3)N1Cc2nc(C(=O)NCc4ccc(N5CCNCC5)cc4)ccc2CC1"),
    # ------- G-series: 4-F-phenyl R1 (smaller) × varied R2 -------
    ("G01","R1=4-F-phenyl, R2=2-pyrrolyl-Bn",
     "O=C(c3ccc(F)cc3)N1Cc2nc(C(=O)NCc4ccccc4-n5cccc5)ccc2CC1"),
    ("G02","R1=4-F-phenyl, R2=4-piperazino-Bn",
     "O=C(c3ccc(F)cc3)N1Cc2nc(C(=O)NCc4ccc(N5CCNCC5)cc4)ccc2CC1"),
    ("G03","R1=4-F-phenyl, R2=4,4-diF-cyclohexyl",
     "O=C(c3ccc(F)cc3)N1Cc2nc(C(=O)NC3CCC(F)(F)CC3)ccc2CC1"),
    # ------- H-series: 2-OMe-pyridin-5-yl R1 (HBD-targeting) × varied R2 -------
    ("H01","R1=2-OMe-pyridin-5-yl, R2=2-pyrrolyl-Bn",
     "O=C(c3cnc(OC)cc3)N1Cc2nc(C(=O)NCc4ccccc4-n5cccc5)ccc2CC1"),
    ("H02","R1=2-OMe-pyridin-5-yl, R2=4-piperazino-Bn",
     "O=C(c3cnc(OC)cc3)N1Cc2nc(C(=O)NCc4ccc(N5CCNCC5)cc4)ccc2CC1"),
    # ------- I-series: 4-CF3-phenyl R1 × varied R2 -------
    ("I01","R1=4-CF3-phenyl, R2=2-pyrrolyl-Bn",
     "O=C(c3ccc(C(F)(F)F)cc3)N1Cc2nc(C(=O)NCc4ccccc4-n5cccc5)ccc2CC1"),
    ("I02","R1=4-CF3-phenyl, R2=4-piperazino-Bn",
     "O=C(c3ccc(C(F)(F)F)cc3)N1Cc2nc(C(=O)NCc4ccc(N5CCNCC5)cc4)ccc2CC1"),
    # ------- J-series: novel designs for TRP stacking / LYS108 H-bond -------
    ("J01","R1=furo[2,3-b]pyridin-2-yl, R2=4-piperazino-Bn",
     "O=C(c3cc4ncccc4o3)N1Cc2nc(C(=O)NCc4ccc(N5CCNCC5)cc4)ccc2CC1"),
    ("J02","R1=benzo[d]isoxazol-3-yl, R2=2-pyrrolyl-Bn",
     "O=C(c3cccc4oncc34)N1Cc2nc(C(=O)NCc4ccccc4-n5cccc5)ccc2CC1"),
    ("J03","R1=2-CF3EtO-py5, R2=3-cyanobenzyl",
     "O=C(c3cnc(OCC(F)(F)F)cc3)N1Cc2nc(C(=O)NCc4cccc(C#N)c4)ccc2CC1"),
    ("J04","R1=2-CF3EtO-py5, R2=4-(dimethylamino)-Bn",
     "O=C(c3cnc(OCC(F)(F)F)cc3)N1Cc2nc(C(=O)NCc4ccc(N(C)C)cc4)ccc2CC1"),
    ("J05","R1=3-Cl-5-CF3-phenyl, R2=2-pyrrolyl-Bn",
     "O=C(c3cc(Cl)cc(C(F)(F)F)c3)N1Cc2nc(C(=O)NCc4ccccc4-n5cccc5)ccc2CC1"),
    ("J06","R1=2-CF3EtO-py5, R2=2-(4-methyl-piperazin-1-yl)-pyrimidine-5-methyl",
     "O=C(c3cnc(OCC(F)(F)F)cc3)N1Cc2nc(C(=O)NCc4cnc(N5CCN(C)CC5)nc4)ccc2CC1"),
]

# Validate each SMILES and compute properties
valid, invalid = [], []
for code, desc, smi in designed:
    m = Chem.MolFromSmiles(smi)
    if m is None:
        invalid.append((code, desc, smi))
    else:
        mw   = Descriptors.ExactMolWt(m)
        logp = Descriptors.MolLogP(m)
        hbd  = rdMolDescriptors.CalcNumHBD(m)
        hba  = rdMolDescriptors.CalcNumHBA(m)
        tpsa = Descriptors.TPSA(m)
        rot  = rdMolDescriptors.CalcNumRotatableBonds(m)
        hac  = m.GetNumHeavyAtoms()
        valid.append(dict(code=code, desc=desc, smiles=smi,
                         mw=mw,logp=logp,hbd=hbd,hba=hba,tpsa=tpsa,rot=rot,hac=hac))

print(f"Valid: {len(valid)}   Invalid: {len(invalid)}")
if invalid:
    print("INVALID SMILES:")
    for code, desc, smi in invalid:
        print(f"  {code}: {smi}")
print()
print(f"{'Code':5s}  {'MW':6s}  {'logP':5s}  {'HBD':4s}  {'HBA':4s}  {'TPSA':5s}  {'RotB':4s}  {'HAC':4s}  Description")
for a in valid:
    print(f"  {a['code']:5s}  {a['mw']:6.0f}  {a['logp']:5.2f}  {a['hbd']:4d}  {a['hba']:4d}  {a['tpsa']:5.0f}  {a['rot']:4d}  {a['hac']:4d}  {a['desc']}")
