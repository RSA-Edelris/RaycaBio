
import os, shutil, zipfile, glob
from collections import Counter

rxn_out = "chemdraw_export/rxn"
os.makedirs(rxn_out, exist_ok=True)
rxn_files = sorted(glob.glob("biovia_rxn/step_*.rxn"))
for fp in rxn_files:
    shutil.copy(fp, os.path.join(rxn_out, os.path.basename(fp)))
print(f"Copied {len(rxn_files)} .rxn → chemdraw_export/rxn/")

with zipfile.ZipFile("compound_A_chemdraw.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for root_d, _, files in os.walk("chemdraw_export"):
        for fn in sorted(files):
            fp = os.path.join(root_d, fn)
            z.write(fp, fp)
    z.write("route_structures.sdf", "sdf/route_structures.sdf")
    if os.path.exists("retrosynthesis_compound_A.png"):
        z.write("retrosynthesis_compound_A.png", "png/retrosynthesis_compound_A.png")

with zipfile.ZipFile("compound_A_chemdraw.zip") as z:
    c = Counter(n.split("/")[1] for n in z.namelist() if "/" in n)
    for k,v in sorted(c.items()):
        print(f"  {k}: {v} files")
    print(f"Total: {len(z.namelist())}")
