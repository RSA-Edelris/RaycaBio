
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter
from rdkit.Chem import ChiralType

def create_enantiomer(mol):
    """Invert all tetrahedral stereocenters to generate the mirror image."""
    rw = Chem.RWMol(Chem.Mol(mol))
    for atom in rw.GetAtoms():
        ct = atom.GetChiralTag()
        if ct == ChiralType.CHI_TETRAHEDRAL_CW:
            atom.SetChiralTag(ChiralType.CHI_TETRAHEDRAL_CCW)
        elif ct == ChiralType.CHI_TETRAHEDRAL_CCW:
            atom.SetChiralTag(ChiralType.CHI_TETRAHEDRAL_CW)
    return rw.GetMol()

# ── classify molecules ────────────────────────────────────────────────────────
input_file = '/home/ubuntu/rayca-artifacts/d43a861c8a85cf7cfd38dce9/files/enantio.sdf'
supplier = Chem.SDMolSupplier(input_file, removeHs=True, sanitize=True)

flat_mols = []   # (2D mol, label)
for mol in supplier:
    if mol is None:
        continue
    name  = mol.GetProp('_Name')
    chiral = Chem.FindMolChiralCenters(mol, includeUnassigned=True)

    if chiral:
        # STERAC = racemic → keep original + add enantiomer
        enant = create_enantiomer(mol)
        flat_mols.append((mol,   f"{name}_ent1"))
        flat_mols.append((enant, f"{name}_ent2"))
        print(f"{name}: {chiral}  →  generating both enantiomers")
    else:
        flat_mols.append((mol, name))
        print(f"{name}: no stereocenters  →  single structure")

print(f"\nTotal structures to process: {len(flat_mols)}")
