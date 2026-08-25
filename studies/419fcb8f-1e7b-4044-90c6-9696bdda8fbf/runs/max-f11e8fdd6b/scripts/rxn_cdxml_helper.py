
import os, sys
from rdkit import Chem
from rdkit.Chem import AllChem
import xml.etree.ElementTree as ET

STEPS = {
    "step_A1": {"reactants": ["O=Cc1cc2c(cc1[N+](=O)[O-])OCO2","NCC1CC1"],       "product": "O=[N+]([O-])c1cc2c(cc1CNCC1CC1)OCO2",                           "label": "NaBH4/MeOH 0C, aza-Michael / reductive amination"},
    "step_A2": {"reactants": ["O=[N+]([O-])c1cc2c(cc1CNCC1CC1)OCO2"],             "product": "CC(C)(C)OC(=O)N(Cc1cc2c(cc1[N+](=O)[O-])OCO2)CC1CC1",           "label": "Boc2O, TEA, DCM, rt"},
    "step_A3": {"reactants": ["CC(C)(C)OC(=O)N(Cc1cc2c(cc1[N+](=O)[O-])OCO2)CC1CC1"], "product": "CC(C)(C)OC(=O)N(Cc1cc2c(cc1N)OCO2)CC1CC1",                "label": "H2 50psi, Pd/C, EtOH"},
    "step_A4": {"reactants": ["CC(C)(C)OC(=O)N(Cc1cc2c(cc1N)OCO2)CC1CC1","CC(C)(C)OC(=O)NCCC(=O)O"], "product": "CC(C)(C)OC(=O)NCCC(=O)Nc1cc2c(cc1CN(CC3CC3)C(=O)OC(C)(C)C)OCO2","label": "HATU, DIPEA, DMF"},
    "step_A5": {"reactants": ["CC(C)(C)OC(=O)NCCC(=O)Nc1cc2c(cc1CN(CC3CC3)C(=O)OC(C)(C)C)OCO2"], "product": "NCCC(=O)Nc1cc2c(cc1CNCC1CC1)OCO2",            "label": "TFA/DCM 1:1, rt"},
    "step_A6": {"reactants": ["NCCC(=O)Nc1cc2c(cc1CNCC1CC1)OCO2"],               "product": "O=C1CCNc2cc3c(cc2CN1CC1CC1)OCO3",                              "label": "PyBOP, DIPEA, DMF, 1mM, rt 24h"},
    "step_B1": {"reactants": ["Nc1cc2c(cc1C3OCCO3)OCO2"],                         "product": "C=CC(=O)Nc1cc2c(cc1C3OCCO3)OCO2",                              "label": "Acryloyl chloride, TEA, DCM, 0C"},
    "step_B2": {"reactants": ["C=CC(=O)Nc1cc2c(cc1C3OCCO3)OCO2","NCC1CC1"],       "product": "O=C(CCNCC1CC1)Nc1cc2c(cc1C3OCCO3)OCO2",                       "label": "Aza-Michael, MeOH, rt"},
    "step_B3": {"reactants": ["O=C(CCNCC1CC1)Nc1cc2c(cc1C3OCCO3)OCO2"],           "product": "O=Cc1cc2c(cc1NC(=O)CCNCC3CC3)OCO2",                           "label": "HCl(aq)/acetone, rt (acetal hydrolysis)"},
    "step_B4": {"reactants": ["O=Cc1cc2c(cc1NC(=O)CCNCC3CC3)OCO2"],               "product": "O=C1CCNc2cc3c(cc2CN1CC1CC1)OCO3",                             "label": "NaBH(OAc)3, DCE, rt (intramol. RA)"},
    "step_B5": {"reactants": ["O=Cc1cc2c(cc1N)OCO2"],                             "product": "Nc1cc2c(cc1C3OCCO3)OCO2",                                      "label": "HOCH2CH2OH, pTsOH, toluene reflux"},
    "step_C1": {"reactants": ["O=Cc1cc2c(cc1Br)OCO2"],                            "product": "OCc1cc2c(cc1Br)OCO2",                                          "label": "NaBH4, MeOH, 0C"},
    "step_C2": {"reactants": ["OCc1cc2c(cc1Br)OCO2"],                             "product": "ClCc1cc2c(cc1Br)OCO2",                                         "label": "SOCl2, DCM, 0C"},
    "step_C3": {"reactants": ["ClCc1cc2c(cc1Br)OCO2","NCC1CC1"],                  "product": "Brc1cc2c(cc1CNCC1CC1)OCO2",                                    "label": "K2CO3, MeCN, rt"},
    "step_C4": {"reactants": ["Brc1cc2c(cc1CNCC1CC1)OCO2","CC(C)(C)OC(=O)NCCC(=O)O"], "product": "CC(C)(C)OC(=O)NCCC(=O)N(Cc1cc2c(cc1Br)OCO2)CC1CC1",    "label": "HATU, DIPEA, DMF"},
    "step_C5": {"reactants": ["CC(C)(C)OC(=O)NCCC(=O)N(Cc1cc2c(cc1Br)OCO2)CC1CC1"], "product": "NCCC(=O)N(Cc1cc2c(cc1Br)OCO2)CC1CC1",                      "label": "TFA/DCM 1:1 (Boc removal)"},
    "step_C6": {"reactants": ["NCCC(=O)N(Cc1cc2c(cc1Br)OCO2)CC1CC1"],             "product": "O=C1CCNc2cc3c(cc2CN1CC1CC1)OCO3",                             "label": "Pd2dba3, XPhos, Cs2CO3, toluene 100C (Buchwald)"},
}

def write_rxn_cdxml(step_name, info, outdir):
    rmols = [Chem.MolFromSmiles(s) for s in info["reactants"]]
    pmol  = Chem.MolFromSmiles(info["product"])
    if any(m is None for m in rmols) or pmol is None:
        return False
    for m in rmols + [pmol]:
        AllChem.Compute2DCoords(m)

    scale = 30.0
    IDC = [100]
    def nid():
        IDC[0] += 1
        return str(IDC[0])

    root = ET.Element("CDXML", BondLength="30")
    page = ET.SubElement(root, "page", id="1", BoundingBox="0 0 900 300",
                          PrintMargins="36 36 36 36")

    def add_mol(mol, x_off):
        conf = mol.GetConformer()
        frag = ET.SubElement(page, "fragment", id=nid())
        amap = {}
        for atom in mol.GetAtoms():
            pos = conf.GetAtomPosition(atom.GetIdx())
            aid = nid()
            amap[atom.GetIdx()] = aid
            el = ET.SubElement(frag, "n", id=aid,
                p=f"{(x_off+pos.x)*scale:.1f} {-pos.y*scale:.1f}",
                Element=str(atom.GetAtomicNum()))
            if atom.GetFormalCharge():
                el.set("Charge", str(atom.GetFormalCharge()))
        for bond in mol.GetBonds():
            bt = str(int(bond.GetBondTypeAsDouble())) if int(bond.GetBondTypeAsDouble()) in (1,2,3) else "1"
            ET.SubElement(frag, "b", id=nid(),
                B=amap[bond.GetBeginAtomIdx()], E=amap[bond.GetEndAtomIdx()], Order=bt)
        conf2 = mol.GetConformer()
        xs = [conf2.GetAtomPosition(j).x for j in range(mol.GetNumAtoms())]
        mol_w = (max(xs)-min(xs)) if len(xs)>1 else 2.0
        return mol_w

    x = 0.0
    for i, mol in enumerate(rmols):
        if i > 0:
            tx = (x+0.5)*scale
            t = ET.SubElement(page, "t", id=nid(), p=f"{tx:.1f} 0", Justification="Center")
            ET.SubElement(t, "s", size="14").text = "+"
            x += 1.5
        mw = add_mol(mol, x)
        x += mw + 3.0

    ax0, ax1 = (x+1)*scale, (x+4)*scale
    ET.SubElement(page, "arrow", id=nid(),
        Head3D=f"{ax1:.1f} 0 0", Tail3D=f"{ax0:.1f} 0 0",
        ArrowheadType="FullArrow")
    t = ET.SubElement(page, "t", id=nid(),
        p=f"{(ax0+ax1)/2:.1f} -22", Justification="Center")
    ET.SubElement(t, "s", size="8").text = info["label"]
    x += 5.0
    add_mol(pmol, x)

    out = os.path.join(outdir, f"{step_name}.cdxml")
    lines = ['<?xml version="1.0" encoding="UTF-8" ?>',
             '<!DOCTYPE CDXML SYSTEM "http://www.cambridgesoft.com/xml/cdxml.dtd" >',
             ET.tostring(root, encoding="unicode")]
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return os.path.exists(out) and os.path.getsize(out) > 0
