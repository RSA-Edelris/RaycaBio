
import urllib.request, gzip, io, os, json
import numpy as np

# ── 1. Download 5EU1 ─────────────────────────────────────────────────────────
url_pdb = "https://files.rcsb.org/download/5EU1.pdb"
with urllib.request.urlopen(url_pdb) as r:
    pdb_text = r.read().decode()

with open("/tmp/5EU1.pdb", "w") as f:
    f.write(pdb_text)
print(f"5EU1 downloaded: {len(pdb_text.splitlines())} lines")

# ── 2. Download AlphaFold model for DCAF16 (Q9NXF7) ─────────────────────────
url_af = "https://alphafold.ebi.ac.uk/files/AF-Q9NXF7-F1-model_v4.pdb"
with urllib.request.urlopen(url_af) as r:
    af_text = r.read().decode()

with open("/tmp/DCAF16_AF.pdb", "w") as f:
    f.write(af_text)
print(f"DCAF16 AF downloaded: {len(af_text.splitlines())} lines")

# ── 3. Quick header scan of 5EU1 ─────────────────────────────────────────────
chains = set()
residues = {}
ligands = []
for line in pdb_text.splitlines():
    if line.startswith("ATOM") or line.startswith("HETATM"):
        chain = line[21]
        resname = line[17:20].strip()
        resseq = line[22:26].strip()
        chains.add(chain)
        if line.startswith("HETATM") and resname not in ("HOH","EDO","PEG","GOL","MES","SO4","PO4","CL","NA"):
            ligands.append((resname, chain, resseq))

print(f"\n5EU1 chains: {sorted(chains)}")
unique_ligs = list(dict.fromkeys(ligands))
print(f"5EU1 non-solvent HETATM records (first 20 unique): {unique_ligs[:20]}")
