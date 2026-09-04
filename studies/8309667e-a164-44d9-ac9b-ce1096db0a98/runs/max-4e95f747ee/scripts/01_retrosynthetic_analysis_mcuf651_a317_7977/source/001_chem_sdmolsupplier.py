
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors

sdf_path = "/home/ubuntu/rayca-artifacts/90d0a82fa1dd72c53f312c76/files/Projets Custom 3.sdf"

supplier = Chem.SDMolSupplier(sdf_path, removeHs=False, sanitize=True)

targets = {}
for mol in supplier:
    if mol is None:
        print("Failed to parse one molecule")
        continue
    props = mol.GetPropsAsDict()
    name = props.get("Column 2", props.get("_Name", "unknown"))
    smi = Chem.MolToSmiles(mol)
    mw = round(Descriptors.ExactMolWt(mol), 2)
    nha = mol.GetNumHeavyAtoms()
    nstereo = len(Chem.FindMolChiralCenters(mol, includeUnassigned=True))
    targets[name] = {"smiles": smi, "mw": mw, "heavy_atoms": nha, "stereocenters": nstereo}
    print(f"{name}: {smi}")
    print(f"  MW={mw}, heavy_atoms={nha}, stereocenters={nstereo}")
    print()
