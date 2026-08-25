
import sys, os, zipfile, shutil
sys.path.insert(0, ".")
from rxn_cdxml_helper import STEPS, write_rxn_cdxml

outdir = "chemdraw_export/rxn_cdxml"
os.makedirs(outdir, exist_ok=True)

ok, fail = [], []
for step_name, info in STEPS.items():
    if write_rxn_cdxml(step_name, info, outdir):
        ok.append(step_name)
    else:
        fail.append(step_name)

print(f"Reaction CDXML: {len(ok)} OK | {len(fail)} FAILED: {fail}")

# Rebuild ZIP with all chemdraw exports
with zipfile.ZipFile("compound_A_chemdraw.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for root_d, _, files in os.walk("chemdraw_export"):
        for fn in sorted(files):
            fp = os.path.join(root_d, fn)
            z.write(fp, fp)
    z.write("route_structures.sdf", "sdf/route_structures.sdf")
    for fn in ["retrosynthesis_compound_A.png"]:
        if os.path.exists(fn):
            z.write(fn, f"png/{fn}")

with zipfile.ZipFile("compound_A_chemdraw.zip") as z:
    from collections import Counter
    c = Counter(n.split("/")[1] for n in z.namelist() if "/" in n)
    for k,v in sorted(c.items()):
        print(f"  {k}: {v} files")
    print(f"Total: {len(z.namelist())}")
