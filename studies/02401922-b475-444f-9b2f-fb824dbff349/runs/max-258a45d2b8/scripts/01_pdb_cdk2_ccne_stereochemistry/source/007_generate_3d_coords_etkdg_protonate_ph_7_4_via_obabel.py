
# Generate 3D coords with ETKDG, then protonate at pH 7.4 via obabel

mol3d = Chem.AddHs(isomers[0])
AllChem.EmbedMolecule(mol3d, AllChem.ETKDGv3())
AllChem.MMFFOptimizeMolecule(mol3d)

# Write pre-protonation SDF
w = Chem.SDWriter('ligand_3d_raw.sdf')
mol3d.SetProp('_Name','CDK2-CCNE_ligand')
w.write(mol3d)
w.close()

# Protonate at pH 7.4 with obabel (-p flag sets protonation state)
result = subprocess.run(
    ['obabel', 'ligand_3d_raw.sdf', '-O', 'ligand_prepared.sdf', '-p', '7.4', '--gen3d'],
    capture_output=True, text=True
)
print("obabel stdout:", result.stdout.strip())
print("obabel stderr:", result.stderr.strip())

# Verify output
suppl2 = Chem.SDMolSupplier('ligand_prepared.sdf', removeHs=False)
ligs = [m for m in suppl2 if m is not None]
print(f"\nPrepared ligands: {len(ligs)}")
for l in ligs:
    nm = l.GetProp('_Name') if l.HasProp('_Name') else 'unknown'
    print(f"  {nm}: {l.GetNumAtoms()} atoms  SMILES={Chem.MolToSmiles(Chem.RemoveHs(l))}")
