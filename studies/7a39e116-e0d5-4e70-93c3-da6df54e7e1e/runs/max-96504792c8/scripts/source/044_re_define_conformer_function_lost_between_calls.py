
from rdkit.Chem import SDWriter, RWMol

# Re-define the conformer function (lost between calls)
def best_3d_conformer(mol, n_confs=50, seed=42):
    mol_h = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    params.numThreads = 4
    n_emb = AllChem.EmbedMultipleConfs(mol_h, numConfs=n_confs, params=params)
    if n_emb == 0:
        raise RuntimeError(f"Embedding failed for {mol.GetProp('_Name')}")
    ff_props = AllChem.MMFFGetMoleculeProperties(mol_h, mmffVariant='MMFF94')
    energies = []
    for cid in range(mol_h.GetNumConformers()):
        ff = AllChem.MMFFGetMoleculeForceField(mol_h, ff_props, confId=cid)
        if ff is None:
            energies.append((float('inf'), cid))
            continue
        ff.Minimize(maxIts=2000)
        energies.append((ff.CalcEnergy(), cid))
    energies.sort()
    best_e, best_cid = energies[0]
    mol_3d = RWMol(Chem.RWMol(mol_h))
    for _, cid in energies[1:]:
        mol_3d.RemoveConformer(cid)
    return mol_3d.GetMol(), best_e, n_emb

# Reload EL2003A-A2U1 from the original file
orig_suppl = Chem.SDMolSupplier(
    '/home/ubuntu/rayca-artifacts/cacaa3ede77705c5b065320a/files/P922_Results.sdf',
    removeHs=False, sanitize=True)
orig_mols = [m for m in orig_suppl if m is not None]
print(f"Original file: {len(orig_mols)} molecule(s)")

# Combine: original + new
all_input_mols = orig_mols + mols   # mols = 5 from P922_Results_2.sdf (still in scope)
print(f"Total to process: {len(all_input_mols)}")

out_path = '/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/ligand_clean_PDK1.sdf'
writer = SDWriter(out_path)

results = []
for mol in all_input_mols:
    name = mol.GetProp('_Name') if mol.HasProp('_Name') else 'unnamed'
    mol.SetProp('_Name', name)

    mol_3d, energy, n_emb = best_3d_conformer(mol)

    for p in mol.GetPropNames():
        mol_3d.SetProp(p, mol.GetProp(p))
    mol_3d.SetProp('_Name', name)
    mol_3d.SetProp('MMFF94_energy_kcal_mol', f'{energy:.4f}')

    Chem.AssignStereochemistry(mol_3d, cleanIt=True, force=True)
    chiral = Chem.FindMolChiralCenters(mol_3d, includeUnassigned=True)
    if chiral:
        mol_3d.SetProp('Note', f"Stereocenters: {chiral}; absolute config retained")
    else:
        mol_3d.SetProp('Note', "No stereocenters; achiral molecule")

    writer.write(mol_3d)
    results.append({'name': name, 'n_emb': n_emb, 'energy': energy, 'n_chiral': len(chiral)})
    print(f"  {name}: {n_emb} confs embedded, best = {energy:.4f} kcal/mol, chiral = {len(chiral)}")

writer.close()
print(f"\nDone. {len(results)} molecules written to ligand_clean_PDK1.sdf")
