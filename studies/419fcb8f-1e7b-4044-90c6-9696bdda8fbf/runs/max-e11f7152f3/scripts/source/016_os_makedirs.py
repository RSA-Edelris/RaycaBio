
import subprocess, os, zipfile

os.makedirs("chemdraw_export/rxn_cdxml", exist_ok=True)

# ── 2. Convert each RXN → CDXML ────────────────────────────────────────
rxn_ok, rxn_fail = [], []
for fn in sorted(os.listdir("biovia_rxn")):
    if not fn.endswith(".rxn"):
        continue
    src  = f"biovia_rxn/{fn}"
    dst  = f"chemdraw_export/rxn_cdxml/{fn.replace('.rxn','.cdxml')}"
    r = subprocess.run(["obabel", src, "-O", dst], capture_output=True, text=True)
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        rxn_ok.append(fn)
    else:
        rxn_fail.append((fn, r.stderr.strip()[:80]))

print(f"RXN→CDXML: {len(rxn_ok)} OK | {len(rxn_fail)} FAILED: {rxn_fail}")

# ── 3. Copy RDF files already written ─────────────────────────────────
import shutil
for fn in os.listdir("biovia_rxn"):
    if fn.endswith(".rdf"):
        shutil.copy(f"biovia_rxn/{fn}", f"chemdraw_export/rdf/{fn}")
print(f"RDF: {os.listdir('chemdraw_export/rdf')}")

# ── 4. Bundle ZIP ──────────────────────────────────────────────────────
with zipfile.ZipFile("compound_A_chemdraw.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk("chemdraw_export"):
        for fn in sorted(files):
            fp = os.path.join(root, fn)
            z.write(fp, fp)
    z.write("route_structures.sdf", "sdf/route_structures.sdf")
    for fn in ["retrosynthesis_compound_A.png","route_A.png","route_B.png","route_C.png"]:
        if os.path.exists(fn):
            z.write(fn, f"png/{fn}")

print("\nZIP contents by folder:")
with zipfile.ZipFile("compound_A_chemdraw.zip") as z:
    from collections import Counter
    c = Counter(n.split("/")[0] for n in z.namelist())
    for k,v in sorted(c.items()): print(f"  {k}: {v} files")
print(f"Total: {len(z.namelist())} files")
