
# Write reaction CDXMLs from SMILES using RDKit 2D coords + CDXML XML writer

import sys, os
sys.path.insert(0, ".")
from rdkit import Chem
from rdkit.Chem import AllChem
import xml.etree.ElementTree as ET

STEPS = {
    # Route A
    "step_A1": {
        "reactants": ["O=Cc1cc2c(cc1[N+](=O)[O-])OCO2", "NCC1CC1"],
        "product":   "O=[N+]([O-])c1cc2c(cc1CNCC1CC1)OCO2",
        "label": "NaBH4 / MeOH / 0°C → rt, 2 h; then reductive amination"
    },
    "step_A2": {
        "reactants": ["O=[N+]([O-])c1cc2c(cc1CNCC1CC1)OCO2"],
        "product":   "CC(C)(C)OC(=O)N(Cc1cc2c(cc1[N+](=O)[O-])OCO2)CC1CC1",
        "label": "Boc2O, TEA, DCM, rt, 12 h"
    },
    "step_A3": {
        "reactants": ["CC(C)(C)OC(=O)N(Cc1cc2c(cc1[N+](=O)[O-])OCO2)CC1CC1"],
        "product":   "CC(C)(C)OC(=O)N(Cc1cc2c(cc1N)OCO2)CC1CC1",
        "label": "H2 (50 psi), Pd/C 10%, EtOH, rt, 4 h"
    },
    "step_A4": {
        "reactants": ["CC(C)(C)OC(=O)N(Cc1cc2c(cc1N)OCO2)CC1CC1", "CC(C)(C)OC(=O)NCCC(=O)O"],
        "product":   "CC(C)(C)OC(=O)NCCC(=O)Nc1cc2c(cc1CN(CC3CC3)C(=O)OC(C)(C)C)OCO2",
        "label": "HATU, DIPEA, DMF, rt, 2 h"
    },
    "step_A5": {
        "reactants": ["CC(C)(C)OC(=O)NCCC(=O)Nc1cc2c(cc1CN(CC3CC3)C(=O)OC(C)(C)C)OCO2"],
        "product":   "NCCC(=O)Nc1cc2c(cc1CNCC1CC1)OCO2",
        "label": "TFA/DCM 1:1, rt, 1 h"
    },
    "step_A6": {
        "reactants": ["NCCC(=O)Nc1cc2c(cc1CNCC1CC1)OCO2"],
        "product":   "O=C1CCNc2cc3c(cc2CN1CC1CC1)OCO3",
        "label": "PyBOP, DIPEA, DMF, 1 mM (high dilution), rt, 24 h"
    },
    # Route B
    "step_B1": {
        "reactants": ["Nc1cc2c(cc1C3OCCO3)OCO2"],
        "product":   "C=CC(=O)Nc1cc2c(cc1C3OCCO3)OCO2",
        "label": "Acryloyl chloride, TEA, DCM, 0°C, 1 h"
    },
    "step_B2": {
        "reactants": ["C=CC(=O)Nc1cc2c(cc1C3OCCO3)OCO2", "NCC1CC1"],
        "product":   "O=C(CCNCC1CC1)Nc1cc2c(cc1C3OCCO3)OCO2",
        "label": "NCC1CC1 (aza-Michael), MeOH, rt, 12 h"
    },
    "step_B3": {
        "reactants": ["O=C(CCNCC1CC1)Nc1cc2c(cc1C3OCCO3)OCO2"],
        "product":   "O=Cc1cc2c(cc1NC(=O)CCNCC3CC3)OCO2",
        "label": "HCl (aq), acetone, rt, 2 h (acetal hydrolysis)"
    },
    "step_B4": {
        "reactants": ["O=Cc1cc2c(cc1NC(=O)CCNCC3CC3)OCO2"],
        "product":   "O=C1CCNc2cc3c(cc2CN1CC1CC1)OCO3",
        "label": "NaBH(OAc)3, DCE, rt, 24 h (intramolecular reductive amination)"
    },
    "step_B5": {
        "reactants": ["O=Cc1cc2c(cc1N)OCO2"],
        "product":   "Nc1cc2c(cc1C3OCCO3)OCO2",
        "label": "HOCH2CH2OH, pTsOH cat, toluene, reflux, 4 h (acetal protection)"
    },
    # Route C
    "step_C1": {
        "reactants": ["O=Cc1cc2c(cc1Br)OCO2"],
        "product":   "OCc1cc2c(cc1Br)OCO2",
        "label": "NaBH4, MeOH, 0°C, 30 min"
    },
    "step_C2": {
        "reactants": ["OCc1cc2c(cc1Br)OCO2"],
        "product":   "ClCc1cc2c(cc1Br)OCO2",
        "label": "SOCl2, DCM, 0°C, 1 h"
    },
    "step_C3": {
        "reactants": ["ClCc1cc2c(cc1Br)OCO2", "NCC1CC1"],
        "product":   "Brc1cc2c(cc1CNCC1CC1)OCO2",
        "label": "K2CO3, MeCN, rt, 4 h (N-alkylation)"
    },
    "step_C4": {
        "reactants": ["Brc1cc2c(cc1CNCC1CC1)OCO2", "CC(C)(C)OC(=O)NCCC(=O)O"],
        "product":   "CC(C)(C)OC(=O)NCCC(=O)N(Cc1cc2c(cc1Br)OCO2)CC1CC1",
        "label": "HATU, DIPEA, DMF, rt, 2 h"
    },
    "step_C5": {
        "reactants": ["CC(C)(C)OC(=O)NCCC(=O)N(Cc1cc2c(cc1Br)OCO2)CC1CC1"],
        "product":   "NCCC(=O)N(Cc1cc2c(cc1Br)OCO2)CC1CC1",
        "label": "TFA/DCM 1:1, rt, 1 h (Boc removal)"
    },
    "step_C6": {
        "reactants": ["NCCC(=O)N(Cc1cc2c(cc1Br)OCO2)CC1CC1"],
        "product":   "O=C1CCNc2cc3c(cc2CN1CC1CC1)OCO3",
        "label": "Pd2dba3, XPhos, Cs2CO3, toluene, 100°C, 12 h (Buchwald-Hartwig)"
    },
}

def mol_to_cdxml_fragment(mol, frag_id_start=1, x_offset=0.0, scale=30.0):
    """Return list of (elem_tag, attrib) tuples representing a CDXML fragment."""
    AllChem.Compute2DCoords(mol)
    conf = mol.GetConformer()
    atoms_xml = []
    bonds_xml = []
    atom_id_map = {}
    for i, atom in enumerate(mol.GetAtoms()):
        aid = frag_id_start + i + 1
        atom_id_map[atom.GetIdx()] = aid
        pos = conf.GetAtomPosition(atom.GetIdx())
        x = x_offset + pos.x * scale
        y = -pos.y * scale   # CDXML y-axis flipped
        attrib = {"id": str(aid), "p": f"{x:.2f} {y:.2f}", "Element": str(atom.GetAtomicNum())}
        charge = atom.GetFormalCharge()
        if charge != 0:
            attrib["Charge"] = str(charge)
        if atom.GetSymbol() != "C" or atom.GetTotalNumHs() > 0:
            attrib["NumHydrogens"] = str(atom.GetTotalNumHs())
        atoms_xml.append(attrib)
    bond_id = frag_id_start + mol.GetNumAtoms() + 1
    for bond in mol.GetBonds():
        bid = bond_id
        bond_id += 1
        btype = {1:"1", 2:"2", 3:"3"}.get(int(bond.GetBondTypeAsDouble()), "1")
        bonds_xml.append({
            "id": str(bid),
            "B": str(atom_id_map[bond.GetBeginAtomIdx()]),
            "E": str(atom_id_map[bond.GetEndAtomIdx()]),
            "Order": btype,
        })
    return atoms_xml, bonds_xml, atom_id_map, bond_id

def write_rxn_cdxml(step_name, step_info, outdir):
    reactant_smiles = step_info["reactants"]
    product_smi = step_info["product"]
    label = step_info["label"]

    reactant_mols = [Chem.MolFromSmiles(s) for s in reactant_smiles]
    product_mol   = Chem.MolFromSmiles(product_smi)
    if any(m is None for m in reactant_mols) or product_mol is None:
        return False

    # Build CDXML XML
    root = ET.Element("CDXML", BondLength="30", CreationProgram="RaycaBio-retrosynthesis")
    page = ET.SubElement(root, "page", id="1", 
                          BoundingBox="0 0 800 400",
                          PrintMargins="36 36 36 36")

    id_counter = 10
    # Place reactants with spacing
    x_cursor = 0.0
    rw = 5.0   # typical mol width in Angstrom
    scale = 30.0

    for i, (mol, smi) in enumerate(zip(reactant_mols, reactant_smiles)):
        AllChem.Compute2DCoords(mol)
        conf = mol.GetConformer()
        xs = [conf.GetAtomPosition(j).x for j in range(mol.GetNumAtoms())]
        mol_w = (max(xs)-min(xs)) if xs else 1.0
        frag = ET.SubElement(page, "fragment", id=str(id_counter))
        id_counter += 1
        atom_ids = {}
        for atom in mol.GetAtoms():
            pos = conf.GetAtomPosition(atom.GetIdx())
            aid = id_counter; id_counter += 1
            atom_ids[atom.GetIdx()] = aid
            a_el = ET.SubElement(frag, "n",
                                 id=str(aid),
                                 p=f"{(x_cursor+pos.x)*scale:.1f} {-pos.y*scale:.1f}",
                                 Element=str(atom.GetAtomicNum()))
            if atom.GetFormalCharge(): a_el.set("Charge", str(atom.GetFormalCharge()))
            if atom.GetNumExplicitHs() or atom.GetTotalNumHs(): a_el.set("NumHydrogens", str(atom.GetTotalNumHs()))
        for bond in mol.GetBonds():
            bid = id_counter; id_counter += 1
            btype = str(int(bond.GetBondTypeAsDouble())) if int(bond.GetBondTypeAsDouble()) in (1,2,3) else "1"
            ET.SubElement(frag, "b",
                          id=str(bid),
                          B=str(atom_ids[bond.GetBeginAtomIdx()]),
                          E=str(atom_ids[bond.GetEndAtomIdx()]),
                          Order=btype)
        x_cursor += mol_w + 4.0
        if i < len(reactant_mols)-1:
            # plus sign text
            tx = (x_cursor - 2.0) * scale
            t = ET.SubElement(page, "t", id=str(id_counter),
                               p=f"{tx:.1f} 0", Justification="Center")
            id_counter += 1
            s = ET.SubElement(t, "s", size="12"); s.text = "+"

    # Arrow
    ax0 = (x_cursor + 1.0) * scale
    ax1 = (x_cursor + 4.0) * scale
    arrow_id = id_counter; id_counter += 1
    ET.SubElement(page, "arrow", id=str(arrow_id),
                  BoundingBox=f"{ax0:.1f} -10 {ax1:.1f} 10",
                  Head3D=f"{ax1:.1f} 0 0", Tail3D=f"{ax0:.1f} 0 0",
                  ArrowheadType="FullArrow")
    # condition label above arrow
    lbl_id = id_counter; id_counter += 1
    t = ET.SubElement(page, "t", id=str(lbl_id),
                       p=f"{(ax0+ax1)/2:.1f} -25", Justification="Center")
    s = ET.SubElement(t, "s", size="8"); s.text = label

    # Product
    x_cursor += 5.0
    AllChem.Compute2DCoords(product_mol)
    conf = product_mol.GetConformer()
    frag = ET.SubElement(page, "fragment", id=str(id_counter)); id_counter += 1
    atom_ids = {}
    for atom in product_mol.GetAtoms():
        pos = conf.GetAtomPosition(atom.GetIdx())
        aid = id_counter; id_counter += 1
        atom_ids[atom.GetIdx()] = aid
        a_el = ET.SubElement(frag, "n", id=str(aid),
                              p=f"{(x_cursor+pos.x)*scale:.1f} {-pos.y*scale:.1f}",
                              Element=str(atom.GetAtomicNum()))
        if atom.GetFormalCharge(): a_el.set("Charge", str(atom.GetFormalCharge()))
    for bond in product_mol.GetBonds():
        bid = id_counter; id_counter += 1
        btype = str(int(bond.GetBondTypeAsDouble())) if int(bond.GetBondTypeAsDouble()) in (1,2,3) else "1"
        ET.SubElement(frag, "b", id=str(bid),
                      B=str(atom_ids[bond.GetBeginAtomIdx()]),
                      E=str(atom_ids[bond.GetEndAtomIdx()]),
                      Order=btype)

    # Write file
    tree = ET.ElementTree(root)
    outpath = os.path.join(outdir, f"{step_name}.cdxml")
    with open(outpath, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8" ?>\n')
        f.write(b'<!DOCTYPE CDXML SYSTEM "http://www.cambridgesoft.com/xml/cdxml.dtd" >\n')
        tree.write(f, encoding="unicode", xml_declaration=False)
    return os.path.exists(outpath) and os.path.getsize(outpath) > 0

outdir = "chemdraw_export/rxn_cdxml"
ok, fail = [], []
for step_name, info in STEPS.items():
    if write_rxn_cdxml(step_name, info, outdir):
        ok.append(step_name)
    else:
        fail.append(step_name)

print(f"Reaction CDXML: {len(ok)} OK | {len(fail)} FAILED: {fail}")
print("Sample:", os.listdir(outdir)[:4])
