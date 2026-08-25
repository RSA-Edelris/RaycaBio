
import zipfile, os
from rdkit import Chem

def molblock(mol, name=""):
    mol.SetProp("_Name", name)
    return Chem.MolToMolBlock(mol)

def write_rdf(path, steps):
    """
    MDL RD file: multiple reactions in one file.
    Biovia Draw opens RDF natively (File > Open).
    """
    lines = ["$RDFILE 1", "$DATM  2026/08/25", ""]
    for step_id, rct_keys, prod_key, cond in steps:
        rct_blocks = [molblock(mols[k], k) for k in rct_keys]
        prd_block  =  molblock(mols[prod_key], prod_key)
        lines += [
            f"$RFMT",
            f"$RXN",
            cond,
            "",
            "  RDKit",
            "",
            f"  {len(rct_blocks):3d}  1",
        ]
        for rb in rct_blocks:
            lines += ["$MOL", rb]
        lines += ["$MOL", prd_block]
        lines += [f"$DTYPE step", f"$DATUM {step_id}", ""]
    with open(path, "w") as f:
        f.write("\n".join(lines))

steps_a = [
    ("A1", ["SM-1","SM-2"],   "Int-A1", "NaBH3CN, AcOH, MeOH, 0C->RT  78%"),
    ("A2", ["Int-A1"],        "Int-A2", "Boc2O, Et3N, DCM, RT  92%"),
    ("A3", ["Int-A2"],        "Int-A3", "SnCl2.2H2O, EtOH, 70C  82%"),
    ("A4", ["Int-A3","SM-4"], "Int-A4", "HATU, DIPEA, DMF, RT  75%"),
    ("A5", ["Int-A4"],        "Int-A5", "TFA/DCM 1:1, RT  quant"),
    ("A6", ["Int-A5"],        "Target", "HATU DIPEA DCM 0.5mM syringe pump  30-35% [WORST STEP]"),
]
steps_b = [
    ("B1", ["SM-6"],          "Int-B1", "HOCH2CH2OH, p-TsOH, toluene, 110C  88%"),
    ("B2", ["Int-B1"],        "Int-B2", "CH2=CHCOCl, Et3N, DCM, 0C  80%"),
    ("B3", ["Int-B2","SM-2"], "Int-B3", "aza-Michael, MeOH, RT, 24h  75%"),
    ("B4", ["Int-B3"],        "Int-B4", "HCl(aq)/acetone, RT  92%"),
    ("B5", ["Int-B4"],        "Target", "NaBH3CN AcOH MeOH/DMF 5mM 40C  38-45%"),
]
steps_c = [
    ("C1", ["SM-7"],          "Int-C1", "NaBH4, MeOH, 0C  96%"),
    ("C2", ["Int-C1"],        "Int-C2", "SOCl2, DCM, 0C  90%"),
    ("C3", ["Int-C2","SM-2"], "Int-C3", "K2CO3, MeCN, 60C  75%"),
    ("C4", ["Int-C3","SM-4"], "Int-C4", "HATU, DIPEA, DMF, RT  82%"),
    ("C5", ["Int-C4"],        "Int-C5", "TFA/DCM 1:1, RT  quant"),
    ("C6", ["Int-C5"],        "Target", "Pd2dba3 3mol% BINAP Cs2CO3 toluene 100C  40-55% [RECOMMENDED]"),
]

write_rdf("biovia_rxn/route_A_all_steps.rdf", steps_a)
write_rdf("biovia_rxn/route_B_all_steps.rdf", steps_b)
write_rdf("biovia_rxn/route_C_all_steps.rdf", steps_c)
print("RDF files written")

# Verify one RXN opens cleanly
rxn = open("biovia_rxn/step_C6.rxn").read()
print("\n--- step_C6.rxn (first 400 chars) ---")
print(rxn[:400])
