
from rdkit.Chem import SDWriter, RWMol

def best_3d_conformer(mol, n_confs=50, seed=42):
    """Add Hs, embed n_confs with ETKDGv3, minimize all with MMFF94, return lowest-energy mol."""
    mol_h = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    params.numThreads = 4
    n_embedded = AllChem.EmbedMultipleConfs(mol_h, numConfs=n_confs, params=params)
    if n_embedded == 0:
        raise RuntimeError("Embedding failed")
    
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
    
    # Keep only best conformer
    mol_3d = RWMol(Chem.RWMol(mol_h))
    for cid in sorted([c for _, c in energies[1:]], reverse=True):
        mol_3d.RemoveConformer(cid)
    
    return mol_3d.GetMol(), best_e, n_embedded

# Process all 5 molecules
out_path = '/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/ligand_clean_PDK1.sdf'
writer = SDWriter(out_path, )

# Append mode: re-open existing file and write new molecules
# First read existing molecule from previous run
existing = list(Chem.SDMolSupplier(out_path, removeHs=False))
print(f"Existing molecules in file: {len(existing)}")

# Write existing + new to output
writer = SDWriter(out_path)
for m in existing:
    writer.write(m)

results = []
for mol in mols:
    name = mol.GetProp('_Name') if mol.HasProp('_Name') else 'unnamed'
    pic50 = mol.GetProp('pIC50 PDK') if mol.HasProp('pIC50 PDK') else ''
    
    mol_3d, energy, n_emb = best_3d_conformer(mol)
    
    # Copy properties
    for p in mol.GetPropNames():
        mol_3d.SetProp(p, mol.GetProp(p))
    mol_3d.SetProp('_Name', name)
    mol_3d.SetProp('MMFF94_energy_kcal_mol', f'{energy:.4f}')
    
    # Note stereo status
    chiral = Chem.FindMolChiralCenters(mol_3d, includeUnassigned=True)
    if chiral:
        note = f"Stereocenters: {chiral}; absolute config retained"
    else:
        note = "No stereocenters; achiral molecule"
    mol_3d.SetProp('Note', note)
    
    writer.write(mol_3d)
    results.append((name, n_emb, energy, len(chiral)))
    print(f"  {name}: {n_emb} conformers embedded, best MMFF94 = {energy:.4f} kcal/mol, chiral centers = {len(chiral)}")

writer.close()
print(f"\nTotal molecules in {out_path}: {len(existing) + len(mols)}")
