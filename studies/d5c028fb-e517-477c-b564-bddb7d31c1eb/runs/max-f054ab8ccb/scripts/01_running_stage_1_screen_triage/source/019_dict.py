
from modulon.governance.toolkit import run_aidd_tool
import shutil

wd = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d'

BOX = dict(boxX=30.57, boxY=5.37, boxZ=-25.80,
           width=24.0, height=20.0, depth=20.0,
           exhaustiveness=8, numModes=9, cnnScoring="rescore", seed=42)

# Batch 1: designed A01-A19
r1 = run_aidd_tool("gnina", inputs={"proteinFile": "receptor_stripped.pdb",
                                     "ligandFile":  "batch_des1.sdf", **BOX})
shutil.copy(f'{wd}/gnina_docked.sdf.gz', f'{wd}/des1_docked.sdf.gz')
print(f"des1 done: rc={r1['rc']}  {r1['output']['summary']}")

# Batch 2: designed A20-A38
r2 = run_aidd_tool("gnina", inputs={"proteinFile": "receptor_stripped.pdb",
                                     "ligandFile":  "batch_des2.sdf", **BOX})
shutil.copy(f'{wd}/gnina_docked.sdf.gz', f'{wd}/des2_docked.sdf.gz')
print(f"des2 done: rc={r2['rc']}  {r2['output']['summary']}")
