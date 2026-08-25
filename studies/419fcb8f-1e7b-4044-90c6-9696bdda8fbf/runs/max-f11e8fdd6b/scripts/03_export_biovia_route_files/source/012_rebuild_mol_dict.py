
from rdkit import Chem
from rdkit.Chem import AllChem
import os

# ── Rebuild mol dict ──────────────────────────────────────────────────────
smiles = {
    "Target":       "O=C1CCNc2cc3c(cc2CN1CC1CC1)OCO3",
    "SM-1":         "O=Cc1cc2c(cc1[N+](=O)[O-])OCO2",
    "SM-2":         "NCC1CC1",
    "SM-4":         "CC(C)(C)OC(=O)NCCC(=O)O",
    "SM-6":         "O=Cc1cc2c(cc1N)OCO2",
    "SM-7":         "O=Cc1cc2c(cc1Br)OCO2",
    "Int-A1":       "O=[N+]([O-])c1cc2c(cc1CNCC1CC1)OCO2",
    "Int-A2":       "CC(C)(C)OC(=O)N(Cc1cc2c(cc1[N+](=O)[O-])OCO2)CC1CC1",
    "Int-A3":       "CC(C)(C)OC(=O)N(Cc1cc2c(cc1N)OCO2)CC1CC1",
    "Int-A4":       "CC(C)(C)OC(=O)NCCC(=O)Nc1cc2c(cc1CN(CC3CC3)C(=O)OC(C)(C)C)OCO2",
    "Int-A5":       "NCCC(=O)Nc1cc2c(cc1CNCC1CC1)OCO2",
    "Int-B1":       "Nc1cc2c(cc1C3OCCO3)OCO2",
    "Int-B2":       "C=CC(=O)Nc1cc2c(cc1C3OCCO3)OCO2",
    "Int-B3":       "O=C(CCNCC1CC1)Nc1cc2c(cc1C3OCCO3)OCO2",
    "Int-B4":       "O=Cc1cc2c(cc1NC(=O)CCNCC3CC3)OCO2",
    "Int-C1":       "OCc1cc2c(cc1Br)OCO2",
    "Int-C2":       "ClCc1cc2c(cc1Br)OCO2",
    "Int-C3":       "Brc1cc2c(cc1CNCC1CC1)OCO2",
    "Int-C4":       "CC(C)(C)OC(=O)NCCC(=O)N(Cc1cc2c(cc1Br)OCO2)CC1CC1",
    "Int-C5":       "NCCC(=O)N(Cc1cc2c(cc1Br)OCO2)CC1CC1",
}

mols = {}
for k, s in smiles.items():
    m = Chem.MolFromSmiles(s)
    AllChem.Compute2DCoords(m)
    mols[k] = m

def molblock(mol, name=""):
    mol.SetProp("_Name", name)
    return Chem.MolToMolBlock(mol)

def write_rxn(path, reactant_keys, product_key, reagent_line="", condition_line=""):
    """Write MDL RXN V2000 file."""
    rct_blocks = [molblock(mols[k], k) for k in reactant_keys]
    prd_block  =  molblock(mols[product_key], product_key)
    lines = [
        "$RXN",
        condition_line or "",
        "",
        f"  RDKit                     ",
        "",
        f"  {len(rct_blocks):3d}  1",
    ]
    for rb in rct_blocks:
        lines += ["$MOL", rb]
    lines += ["$MOL", prd_block]
    with open(path, "w") as f:
        f.write("\n".join(lines))

os.makedirs("biovia_rxn", exist_ok=True)

# Route A
steps_a = [
    ("A1", ["SM-1","SM-2"],   "Int-A1", "NaBH3CN, AcOH, MeOH, 0C->RT, 78%"),
    ("A2", ["Int-A1"],        "Int-A2", "Boc2O, Et3N, DCM, RT, 92%"),
    ("A3", ["Int-A2"],        "Int-A3", "SnCl2.2H2O, EtOH, 70C, 82%"),
    ("A4", ["Int-A3","SM-4"], "Int-A4", "HATU, DIPEA, DMF, RT, 75%"),
    ("A5", ["Int-A4"],        "Int-A5", "TFA/DCM 1:1, RT, quant"),
    ("A6", ["Int-A5"],        "Target", "HATU, DIPEA, DCM 0.5mM, syringe pump, 30-35% WORST STEP"),
]
# Route B
steps_b = [
    ("B1", ["SM-6"],          "Int-B1", "HOCH2CH2OH, p-TsOH, toluene, 110C, 88%"),
    ("B2", ["Int-B1"],        "Int-B2", "CH2=CHCOCl, Et3N, DCM, 0C, 80%"),
    ("B3", ["Int-B2","SM-2"], "Int-B3", "aza-Michael, MeOH, RT, 24h, 75%"),
    ("B4", ["Int-B3"],        "Int-B4", "HCl(aq)/acetone, RT, 92%"),
    ("B5", ["Int-B4"],        "Target", "NaBH3CN, AcOH, MeOH/DMF 5mM, 40C, 38-45%"),
]
# Route C
steps_c = [
    ("C1", ["SM-7"],          "Int-C1", "NaBH4, MeOH, 0C, 96%"),
    ("C2", ["Int-C1"],        "Int-C2", "SOCl2, DCM, 0C, 90%"),
    ("C3", ["Int-C2","SM-2"], "Int-C3", "K2CO3, MeCN, 60C, 75%"),
    ("C4", ["Int-C3","SM-4"], "Int-C4", "HATU, DIPEA, DMF, RT, 82%"),
    ("C5", ["Int-C4"],        "Int-C5", "TFA/DCM 1:1, RT, quant"),
    ("C6", ["Int-C5"],        "Target", "Pd2dba3 3mol%, BINAP, Cs2CO3, toluene 100C, 40-55% RECOMMENDED"),
]

for step_id, rcts, prod, cond in steps_a + steps_b + steps_c:
    write_rxn(f"biovia_rxn/step_{step_id}.rxn", rcts, prod, cond)

written = os.listdir("biovia_rxn")
print(f"Written {len(written)} RXN files: {sorted(written)}")
