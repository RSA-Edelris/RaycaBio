
import gzip
from rdkit import Chem
import pandas as pd

wd = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d'

def parse_docked(gz_path):
    rows = []
    with gzip.open(gz_path, 'rt') as fh:
        content = fh.read()
    supp = Chem.SDMolSupplier()
    supp.SetData(content, removeHs=False)
    for m in supp:
        if m is None:
            continue
        name = m.GetProp('_Name').strip()
        props = m.GetPropsAsDict()
        affinity    = float(props.get('minimizedAffinity', props.get('affinity', 0.0)))
        cnn_score   = float(props.get('CNNscore',   props.get('cnn_pose_score', 0.0)))
        cnn_aff     = float(props.get('CNNaffinity', props.get('cnn_affinity', 0.0)))
        rows.append({'name': name, 'vina': affinity, 'cnn_score': cnn_score, 'cnn_aff': cnn_aff})
    return rows

all_rows = []
for tag, path in [('actives', f'{wd}/actives_docked.sdf.gz'),
                  ('des1',    f'{wd}/des1_docked.sdf.gz'),
                  ('des2',    f'{wd}/des2_docked.sdf.gz')]:
    rows = parse_docked(path)
    print(f"{tag}: {len(rows)} poses")
    all_rows.extend(rows)

df = pd.DataFrame(all_rows)
# Best pose per compound = most negative Vina (or highest CNN score for equal Vina)
best = (df.sort_values('vina')
          .groupby('name', sort=False)
          .first()
          .reset_index())
print(f"\nTotal unique compounds docked: {len(best)}")
print(best.sort_values('vina').head(10).to_string(index=False))
