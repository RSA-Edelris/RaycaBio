
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter

mols_in = [m for m in Chem.SDMolSupplier(lig_sdf, removeHs=True, sanitize=True) if m is not None]

ligand_data = []
for m in mols_in:
    name = next((m.GetProp(k) for k in ('_Name','Name','Molecule Name') 
                 if m.HasProp(k) and m.GetProp(k).strip()), 'unnamed')
    smi  = Chem.MolToSmiles(m)
    pic50 = m.GetProp('pIC50 PDK') if m.HasProp('pIC50 PDK') else ''
    ligand_data.append({'name': name, 'smiles': smi, 'pic50': pic50})
    print(f"  {name}: {smi}")

print(f"\nTotal: {len(ligand_data)} ligands")
