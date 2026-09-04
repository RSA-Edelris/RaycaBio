
# Prepare ligand PDBQT with meeko (handles rotatable bonds, charges, pH protonation)
from meeko import MoleculePreparation, PDBQTWriterLegacy

suppl_lig = Chem.SDMolSupplier('ligand_prepared.sdf', removeHs=False)
mol_lig = [m for m in suppl_lig if m is not None][0]

preparator = MoleculePreparation()
mol_setup_list = preparator.prepare(mol_lig)
setup = mol_setup_list[0]

pdbqt_str, is_ok, err = PDBQTWriterLegacy.write_string(setup)
if not is_ok:
    print("PDBQT write error:", err)
else:
    with open('ligand.pdbqt', 'w') as f:
        f.write(pdbqt_str)
    print(f"ligand.pdbqt written: {len(pdbqt_str)} chars")
    rot_bonds = pdbqt_str.count('BRANCH')
    print(f"Rotatable bonds: {rot_bonds}")

# Also prepare CTX reference PDBQT
suppl_ctx2 = Chem.SDMolSupplier('ctx_ref.sdf', removeHs=False)
mol_ctx = [m for m in suppl_ctx2 if m is not None][0]
ctx_setup_list = preparator.prepare(mol_ctx)
ctx_pdbqt, is_ok2, err2 = PDBQTWriterLegacy.write_string(ctx_setup_list[0])
if is_ok2:
    with open('ctx_ref.pdbqt', 'w') as f:
        f.write(ctx_pdbqt)
    print(f"ctx_ref.pdbqt written")
else:
    print("CTX PDBQT error:", err2)
