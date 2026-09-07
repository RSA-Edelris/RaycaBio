
import gzip
from rdkit import Chem
from rdkit.Chem import SDWriter
import subprocess

# ── Write combined poses SDF + best-pose complex PDB per ligand ───────────────
def read_gnina_gz(gz_path, ligand_name):
    with gzip.open(gz_path, 'rt') as fh:
        sdf_text = fh.read()
    suppl = Chem.SDMolSupplier()
    suppl.SetData(sdf_text, removeHs=False)
    mols = []
    for i, mol in enumerate(suppl):
        if mol is None:
            continue
        mol.SetProp('Ligand', ligand_name)
        mol.SetProp('Pose', str(i + 1))
        mols.append(mol)
    return mols

# Re-read all pose mols (functions don't persist across cells)
for name, _ in lig_sdf_paths:
    gz = f'docked_{name}.sdf.gz'
    mols = read_gnina_gz(gz, name)
    all_docking[name]['poses_mols'] = mols

# Write per-ligand 5-pose SDF
for name, entry in all_docking.items():
    mols = entry['poses_mols']
    out_sdf = f'poses_{name}.sdf'
    w = SDWriter(out_sdf)
    for mol in mols:
        w.write(mol)
    w.close()
    print(f"Written {out_sdf} ({len(mols)} poses)")

# ── Print docking summary to pick best pose for MM-GBSA ──────────────────────
print("\nDocking summary (by CNN pose score, best pose per ligand):")
summary_rows = []
for name, entry in all_docking.items():
    out = entry['output']
    poses = out.get('poses', [])
    best = sorted(poses, key=lambda p: -p.get('cnn_pose_score', 0))[0] if poses else {}
    row = {
        'name':       name,
        'best_vina':  out.get('best_affinity_kcal_mol'),
        'best_cnn_aff': out.get('best_cnn_affinity'),
        'best_cnn_pose': out.get('best_cnn_pose_score'),
        'all_poses':  poses,
        'best_pose_rank': best.get('rank', 1),
    }
    summary_rows.append(row)
    print(f"  {name}: vina={row['best_vina']} kcal/mol  "
          f"cnn_aff={row['best_cnn_aff']}  cnn_pose={row['best_cnn_pose']}")

# ── Check MM-GBSA tooling ─────────────────────────────────────────────────────
print("\nChecking MM-GBSA tooling:")
for pkg in ['openmmforcefields', 'openff.toolkit', 'parmed', 'openmm']:
    try:
        __import__(pkg.replace('.', '_') if '.' in pkg else pkg)
        print(f"  {pkg}: available")
    except ImportError:
        try:
            import importlib; importlib.import_module(pkg)
            print(f"  {pkg}: available")
        except:
            print(f"  {pkg}: NOT found")
