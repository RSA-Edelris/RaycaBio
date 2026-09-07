
# ── parse fpocket info.txt ────────────────────────────────────────────────────
info_path = f"{WORK}/4CI2_receptor_noh_info.txt"
info_text = open(info_path).read()

# extract pocket blocks
import re
pocket_blocks = re.split(r"Pocket\s+\d+\s*:", info_text)[1:]  # skip header

pocket_data = []
for i, blk in enumerate(pocket_blocks):
    def gf(key):
        m = re.search(rf"{re.escape(key)}\s*:\s*([-\d.]+)", blk)
        return float(m.group(1)) if m else None
    pocket_data.append({
        "pocket": i+1,
        "score":       gf("Druggability Score"),
        "volume":      gf("Volume"),
        "mean_lp":     gf("Mean local hydrophobic density Score"),
        "polar_asp":   gf("Polarity score"),
        "center_x":    None,  # not in info.txt; will use pocket atom PDB
    })

# show top 10 by druggability
ranked = sorted(pocket_data, key=lambda x: x["score"] or 0, reverse=True)
print("Pocket  DrugScore  Volume")
for p in ranked[:10]:
    print(f"  #{p['pocket']:3d}  {p['score']:.3f}     {p['volume']:.0f} Å³")

# ── compute distance from each pocket's atoms to LVY centroid ────────────────
# read pocket*_atm.pdb files
import glob
atm_files = sorted(glob.glob(f"{WORK}/pocket*_atm.pdb"))
print(f"\nFound {len(atm_files)} pocket atom files")

pocket_centers = {}
for pf in atm_files:
    pnum = int(re.search(r"pocket(\d+)_atm", pf).group(1))
    coords = []
    with open(pf) as f:
        for line in f:
            if line[:6].strip() in ("ATOM","HETATM"):
                try:
                    x,y,z = float(line[30:38]),float(line[38:46]),float(line[46:54])
                    coords.append([x,y,z])
                except: pass
    if coords:
        c = np.array(coords).mean(axis=0)
        pocket_centers[pnum] = c

# rank by distance to LVY centroid
dist_ranked = sorted(pocket_centers.items(), key=lambda kv: np.linalg.norm(kv[1]-centroid))
print("\nPocket  dist_to_LVY  center")
for pnum, ctr in dist_ranked[:10]:
    d = np.linalg.norm(ctr - centroid)
    sc = next((p["score"] for p in pocket_data if p["pocket"]==pnum), "?")
    print(f"  #{pnum:3d}  {d:6.1f} Å   ({ctr[0]:.1f},{ctr[1]:.1f},{ctr[2]:.1f})  score={sc}")

best_fpocket = dist_ranked[0][0]
best_fp_center = dist_ranked[0][1]
best_fp_score  = next((p["score"] for p in pocket_data if p["pocket"]==best_fpocket), None)
print(f"\n✓ Pocket #{best_fpocket} is closest to LVY ({np.linalg.norm(best_fp_center-centroid):.1f} Å), score={best_fp_score}")
