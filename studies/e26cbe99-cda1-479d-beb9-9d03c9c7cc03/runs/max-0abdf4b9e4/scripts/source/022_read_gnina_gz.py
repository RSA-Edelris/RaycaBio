
import gzip, os, shutil
from rdkit import Chem
from rdkit.Chem import SDWriter

def read_gnina_gz(gz_path, ligand_name):
    """Parse gnina output gz, tag poses with ligand name, return list of mols."""
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

# ── Save ent1 result already in hand ─────────────────────────────────────────
shutil.copy('gnina_docked.sdf.gz', 'docked_EDS01357518_ent1.sdf.gz')
all_docking = {}
all_docking['EDS01357518_ent1'] = {
    'output': r_gnina['output'],
    'poses_mols': read_gnina_gz('docked_EDS01357518_ent1.sdf.gz', 'EDS01357518_ent1'),
}
print(f"EDS01357518_ent1: {len(all_docking['EDS01357518_ent1']['poses_mols'])} poses saved")

# ── Dock remaining 4 ligands ──────────────────────────────────────────────────
for name, lig_path in lig_sdf_paths[1:]:   # skip ent1 (already done)
    print(f"\nDocking {name} ...")
    r = run_aidd_tool('gnina', {
        'proteinFile':    trimmed_noh_path,
        'ligandFile':     lig_path,
        'boxX':           pocket_cx,
        'boxY':           pocket_cy,
        'boxZ':           pocket_cz,
        'width':          BOX_SZ,
        'height':         BOX_SZ,
        'depth':          BOX_SZ,
        'numModes':       5,
        'exhaustiveness': 16,
        'cnnScoring':     'rescore',
        'seed':           42,
    })
    rc = r.get('rc')
    out = r.get('output', {})
    print(f"  rc={rc}  best_vina={out.get('best_affinity_kcal_mol')} kcal/mol  "
          f"cnn_pose={out.get('best_cnn_pose_score')}  cnn_aff={out.get('best_cnn_affinity')}")

    gz_out = f'docked_{name}.sdf.gz'
    shutil.copy('gnina_docked.sdf.gz', gz_out)
    all_docking[name] = {
        'output': out,
        'poses_mols': read_gnina_gz(gz_out, name),
    }
    print(f"  Poses: {len(all_docking[name]['poses_mols'])}")

print(f"\n{'='*60}")
print(f"All dockings complete: {list(all_docking.keys())}")
