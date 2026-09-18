
import numpy as np, urllib.request, json

# ── 1. Full per-residue pLDDT profile for DCAF16 ────────────────────────────
af_residues = {}
for line in af_text.splitlines():
    if line.startswith("ATOM") and line[12:16].strip() == "CA":
        resseq  = int(line[22:26])
        resname = line[17:20].strip()
        plddt   = float(line[60:66])
        af_residues[resseq] = {"resname": resname, "plddt": plddt}

plddts = [v["plddt"] for v in af_residues.values()]
print(f"DCAF16 residues: {len(af_residues)}")
print(f"pLDDT  mean={np.mean(plddts):.1f}  median={np.median(plddts):.1f}  "
      f"max={np.max(plddts):.1f}  min={np.min(plddts):.1f}")

# Fraction in each confidence tier
tiers = {"very_high(>90)":0,"confident(70-90)":0,"low(50-70)":0,"very_low(<50)":0}
for p in plddts:
    if p > 90:   tiers["very_high(>90)"] += 1
    elif p > 70: tiers["confident(70-90)"] += 1
    elif p > 50: tiers["low(50-70)"] += 1
    else:        tiers["very_low(<50)"] += 1
for k,v in tiers.items():
    print(f"  {k}: {v} ({v/len(plddts):.1%})")

# Highest confidence stretch
runs = []
cur_start, cur_sum, cur_n = None, 0, 0
for rseq in sorted(af_residues):
    p = af_residues[rseq]["plddt"]
    if p > 50:
        if cur_start is None: cur_start, cur_sum, cur_n = rseq, 0, 0
        cur_sum += p; cur_n += 1
    else:
        if cur_start is not None and cur_n >= 3:
            runs.append((cur_start, rseq-1, cur_sum/cur_n, cur_n))
        cur_start = None
if cur_start and cur_n >= 3:
    runs.append((cur_start, sorted(af_residues)[-1], cur_sum/cur_n, cur_n))
print("\nConfident stretches (≥3 consecutive residues with pLDDT>50):")
for s,e,avg,n in sorted(runs, key=lambda x:-x[2]):
    print(f"  res {s}-{e}  len={n}  avg_pLDDT={avg:.1f}")

# ── 2. Detailed cysteine microenvironment ────────────────────────────────────
af_atoms = []
for line in af_text.splitlines():
    if line.startswith("ATOM"):
        af_atoms.append({
            "name": line[12:16].strip(),
            "resname": line[17:20].strip(),
            "resseq": int(line[22:26]),
            "x": float(line[30:38]),
            "y": float(line[38:46]),
            "z": float(line[46:54]),
            "plddt": float(line[60:66])
        })

af_xyz = np.array([[a["x"],a["y"],a["z"]] for a in af_atoms])
af_ca  = np.array([[a["x"],a["y"],a["z"]] for a in af_atoms if a["name"]=="CA"])

print("\nDCAF16 cysteine characterization:")
print(f"{'CYS':>4} {'pLDDT':>7} {'Nbr_Ca_8A':>10} {'NeighborRes'}")
for c in cys_records:
    xyz = np.array([c["x"], c["y"], c["z"]])
    dists_ca = np.linalg.norm(af_ca - xyz, axis=1)
    n_ca_8  = int((dists_ca < 8.0).sum()) - 1   # exclude self
    # neighbor residue names
    ca_records = [a for a in af_atoms if a["name"]=="CA"]
    neighbors = [ca_records[i]["resseq"] for i,d in enumerate(dists_ca) 
                 if d < 8.0 and ca_records[i]["resseq"] != c["resseq"]]
    # heavy atom contact count (all-atom <5Å, excluding own residue)
    own_res = c["resseq"]
    other_xyz = np.array([[a["x"],a["y"],a["z"]] for a in af_atoms if a["resseq"]!=own_res])
    n_heavy = int((np.linalg.norm(other_xyz - xyz, axis=1) < 5.0).sum())
    print(f"C{c['resseq']:>3}  {c['plddt']:>7.1f}  {n_ca_8:>10d}   {sorted(neighbors)}")
    
# ── 3. Search PDB for experimental DCAF16 structures ────────────────────────
search_url = ("https://search.rcsb.org/rcsbsearch/v2/query?"
              "json=%7B%22query%22%3A%7B%22type%22%3A%22terminal%22%2C"
              "%22service%22%3A%22text%22%2C%22parameters%22%3A%7B"
              "%22value%22%3A%22DCAF16%22%7D%7D%2C%22return_type%22%3A%22entry%22%7D")
try:
    with urllib.request.urlopen(search_url, timeout=10) as r:
        hits = json.loads(r.read().decode())
    ids = [h["identifier"] for h in hits.get("result_set",[])]
    print(f"\nPDB search for 'DCAF16': {len(ids)} hits → {ids[:15]}")
except Exception as e:
    print(f"\nPDB search failed: {e}")
