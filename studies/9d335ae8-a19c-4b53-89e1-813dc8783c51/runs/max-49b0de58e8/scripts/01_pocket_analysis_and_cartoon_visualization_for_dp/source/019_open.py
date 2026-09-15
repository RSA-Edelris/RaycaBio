
import numpy as np
from scipy.spatial import cKDTree
from sklearn.cluster import DBSCAN

PDB = "/home/ubuntu/rayca-artifacts/0e2dd53329c8b2ef8e1bf379/files/dpCDK2-CCNE1_without ligand.pdb"

# ── Parse all ATOM records ───────────────────────────────────────────────────
atoms = []
with open(PDB) as f:
    for line in f:
        rec = line[:6].strip()
        if rec not in ("ATOM", "HETATM"):
            continue
        try:
            atoms.append(dict(
                rec     = rec,
                name    = line[12:16].strip(),
                resname = line[17:20].strip(),
                chain   = line[21].strip(),
                resseq  = int(line[22:26]),
                x = float(line[30:38]),
                y = float(line[38:46]),
                z = float(line[46:54])
            ))
        except:
            pass

protein = [a for a in atoms if a['rec']=='ATOM']
waters  = [a for a in atoms if a['resname']=='HOH']

chains = {}
for a in protein:
    chains.setdefault(a['chain'], set()).add(a['resseq'])

print(f"Total protein atoms: {len(protein)}")
for ch, rids in sorted(chains.items()):
    print(f"  Chain {ch}: res {min(rids)} – {max(rids)}  ({len(rids)} residues)")
print(f"Waters: {len(waters)}")

# Separate chains
cdk2  = [a for a in protein if a['chain'] == 'A']
ccne1 = [a for a in protein if a['chain'] == 'B']
print(f"\nCDK2 atoms:   {len(cdk2)}")
print(f"CyclinE1 atoms: {len(ccne1)}")
