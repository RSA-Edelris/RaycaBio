
import gzip, os
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors

wd = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d'
os.makedirs(f'{wd}/md_prep', exist_ok=True)

def extract_best_poses(gz_path):
    """Return dict of name -> rank-1 mol (first occurrence per name)."""
    with gzip.open(gz_path, 'rt') as fh:
        content = fh.read()
    supp = Chem.SDMolSupplier()
    supp.SetData(content, removeHs=False)
    best = {}
    for m in supp:
        if m is None: continue
        name = m.GetProp('_Name').strip()
        if name not in best:
            best[name] = m
    return best

act_poses = extract_best_poses(f'{wd}/actives_docked.sdf.gz')
ina_poses = extract_best_poses(f'{wd}/inactives_docked.sdf.gz')

all_cpd_ids = {
    'actives':   ['EDS00495858', 'EDS00480994', 'EDS00444974'],
    'inactives': ['EDS00481054', 'EDS00441134', 'EDS00445742'],
}
all_poses = {**act_poses, **ina_poses}

print("Best docking poses extracted:")
for cls, ids in all_cpd_ids.items():
    for cid in ids:
        m = all_poses.get(cid)
        if m is None:
            print(f"  {cid}: NOT FOUND")
            continue
        props = m.GetPropsAsDict()
        aff  = props.get('minimizedAffinity', props.get('affinity', '?'))
        cnn  = props.get('CNNscore', '?')
        cnn_aff = props.get('CNNaffinity', '?')
        # Write individual SDF for acpype
        out_sdf = f'{wd}/md_prep/{cid}_pose.sdf'
        w = Chem.SDWriter(out_sdf)
        w.write(m)
        w.close()
        print(f"  [{cls}] {cid}: Vina={aff:.2f}  CNNscore={cnn:.3f}  CNNaff={cnn_aff:.3f}  -> {out_sdf.split('/')[-1]}")

print("\nAll pose SDFs written to md_prep/")
