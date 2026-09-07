
from rdkit.Chem import SDWriter, RWMol

def get_mol_name(mol):
    """Try _Name (title line), then SDF Name/Molecule Name fields."""
    for key in ('_Name', 'Name', 'Molecule Name'):
        try:
            v = mol.GetProp(key)
            if v and v.strip():
                return v.strip()
        except KeyError:
            pass
    return 'unnamed'

def best_3d_conformer(mol, n_confs=50, seed=42):
    mol_h = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    params.numThreads = 4
    AllChem.EmbedMultipleConfs(mol_h, numConfs=n_confs, params=params)
    n_emb = mol_h.GetNumConformers()
    if n_emb == 0:
        raise RuntimeError(f"Embedding failed")
    ff_props = AllChem.MMFFGetMoleculeProperties(mol_h, mmffVariant='MMFF94')
    energies = []
    for cid in range(n_emb):
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

# Reload both input files fresh
orig_mols = [m for m in Chem.SDMolSupplier(
    '/home/ubuntu/rayca-artifacts/cacaa3ede77705c5b065320a/files/P922_Results.sdf',
    removeHs=False, sanitize=True) if m is not None]

new_mols  = [m for m in Chem.SDMolSupplier(
    '/home/ubuntu/rayca-artifacts/cacaa3ede77705c5b065320a/files/P922_Results_2.sdf',
    removeHs=False, sanitize=True) if m is not None]

all_input = orig_mols + new_mols
print(f"Processing {len(all_input)} molecules (1 original + 5 new)\n")

out_path = '/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/ligand_clean_PDK1.sdf'
writer = SDWriter(out_path)

final_results = []
for mol in all_input:
    name = get_mol_name(mol)
    mol.SetProp('_Name', name)

    mol_3d, energy, n_emb = best_3d_conformer(mol)

    # Copy all SDF properties
    for p in mol.GetPropNames():
        if not p.startswith('_'):
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
    final_results.append({'name': name, 'n_emb': n_emb, 'energy': energy,
                          'n_chiral': len(chiral), 'chiral': chiral})
    print(f"  {name:20s}  confs={n_emb}  best={energy:10.4f} kcal/mol  chiral={chiral if chiral else 'none'}")

writer.close()

print(f"\n{'='*60}")
print(f"ligand_clean_PDK1.sdf written: {len(final_results)} molecules")

# Quick read-back verification
check = [m for m in Chem.SDMolSupplier(out_path, removeHs=False) if m is not None]
print(f"Verification read-back: {len(check)} molecules OK")
for m in check:
    conf = m.GetConformer()
    z = conf.GetPositions()[:,2]
    print(f"  {get_mol_name(m):20s}  Z=[{z.min():.2f},{z.max():.2f}]  atoms={m.GetNumAtoms()}")
