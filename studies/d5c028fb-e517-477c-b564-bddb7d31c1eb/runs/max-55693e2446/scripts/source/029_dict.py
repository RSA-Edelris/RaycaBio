
from modulon.governance.toolkit import run_aidd_tool
import shutil, gzip
from rdkit import Chem

wd = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d'

BOX = dict(boxX=30.57, boxY=5.37, boxZ=-25.80,
           width=24.0, height=20.0, depth=20.0,
           exhaustiveness=8, numModes=9, cnnScoring="rescore", seed=42)

r = run_aidd_tool("gnina", inputs={"proteinFile": "receptor_stripped.pdb",
                                    "ligandFile":  "inactives_for_dock.sdf", **BOX})
shutil.copy(f'{wd}/gnina_docked.sdf.gz', f'{wd}/inactives_docked.sdf.gz')
print(r['output']['summary'])
print(f"rc={r['rc']}  gpu={r['gpu']}  t={r['duration_s']:.0f}s")

# Count poses
with gzip.open(f'{wd}/inactives_docked.sdf.gz', 'rt') as fh:
    content = fh.read()
print(f"Poses in inactives_docked.sdf.gz: {content.count('$$$$')}")
