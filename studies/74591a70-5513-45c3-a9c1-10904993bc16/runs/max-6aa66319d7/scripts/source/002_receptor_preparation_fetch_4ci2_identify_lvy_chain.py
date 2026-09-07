
# ─── RECEPTOR PREPARATION ──────────────────────────────────────────────────────
# Fetch 4CI2, identify LVY chain, fill loops, protonate pH 7.4, keep site waters
# ──────────────────────────────────────────────────────────────────────────────
import urllib.request, os, json
import numpy as np

WORK = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"

# ── 1. Download raw PDB ────────────────────────────────────────────────────────
raw_pdb = f"{WORK}/4CI2_raw.pdb"
urllib.request.urlretrieve("https://files.rcsb.org/download/4CI2.pdb", raw_pdb)
print(f"Downloaded {os.path.getsize(raw_pdb):,} bytes → {raw_pdb}")

# ── 2. Inspect chains and ligands ──────────────────────────────────────────────
chains, hets = set(), {}
with open(raw_pdb) as f:
    for line in f:
        rec = line[:6].strip()
        if rec in ("ATOM", "HETATM"):
            ch = line[21]
            chains.add(ch)
        if rec == "HETATM":
            resn = line[17:20].strip()
            if resn not in ("HOH","WAT"):
                hets[resn] = hets.get(resn, 0) + 1

print(f"Chains: {sorted(chains)}")
print(f"HET groups: {dict(sorted(hets.items(), key=lambda x:-x[1]))}")
