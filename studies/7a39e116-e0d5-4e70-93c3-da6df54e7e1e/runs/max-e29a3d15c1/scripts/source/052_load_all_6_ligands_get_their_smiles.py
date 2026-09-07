
from rdkit.Chem import AllChem, SDWriter, RWMol

# Load all 6 ligands and get their SMILES
mols_in = [m for m in Chem.SDMolSupplier(lig_sdf, removeHs=True, sanitize=True) if m is not None]

ligand_data = []
for m in mols_in:
    name = m.GetProp('_Name') if m.HasProp('_Name') else (
           m.GetProp('Name') if m.HasProp('Name') else 'unnamed')
    smi  = Chem.MolToSmiles(m)
    pic50 = m.GetProp('pIC50 PDK') if m.HasProp('pIC50 PDK') else ''
    ligand_data.append({'name': name, 'smiles': smi, 'pic50': pic50, 'mol': m})
    print(f"  {name}: {smi}")

print(f"\nTotal: {len(ligand_data)} ligands")
