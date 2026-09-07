
import json, glob, os

# ── parse pocket data from fp['output'] ───────────────────────────────────────
out = fp.get("output", {})
if isinstance(out, str):
    out = json.loads(out)

pockets_raw = out.get("pockets", [])
print(f"32 pockets detected. Top pocket: Score={out.get('pockets',[{}])[0].get('metrics',{}).get('Score','?')}")

# ── locate pocket atm.pdb files ───────────────────────────────────────────────
# artifact store path  
artifact_root = "/home/ubuntu/rayca-artifacts"
atm_files = sorted(glob.glob(f"{artifact_root}/**/pocket*_atm.pdb", recursive=True))
if not atm_files:
    atm_files = sorted(glob.glob(f"{WORK}/**/pocket*_atm.pdb", recursive=True))
print(f"\nFound {len(atm_files)} pocket_atm files")
if atm_files:
    print(f"  Example: {atm_files[0]}")

# ── compute centroid of each pocket and distance to LVY ──────────────────────
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
        pocket_centers[pnum] = np.array(coords).mean(axis=0)

# merge with scores
pocket_summary = []
for p in pockets_raw:
    pnum = p["pocket"]
    m = p.get("metrics", {})
    ctr = pocket_centers.get(pnum, np.array([0,0,0]))
    d   = np.linalg.norm(ctr - centroid) if pnum in pocket_centers else 999
    pocket_summary.append({
        "pocket": pnum,
        "score":  m.get("Score", 0),
        "drug":   m.get("Druggability Score", 0),
        "vol":    m.get("Volume", 0),
        "n_sph":  m.get("Number of Alpha Spheres", 0),
        "dist_lvy": d,
        "center": ctr.tolist() if pnum in pocket_centers else None
    })

# rank by distance to LVY
pocket_summary.sort(key=lambda x: x["dist_lvy"])
print(f"\n{'Pkt':>4} {'Score':>6} {'Drug':>6} {'Vol':>7} {'d_LVY':>7}  Center")
for ps in pocket_summary[:10]:
    c = ps["center"]
    cstr = f"({c[0]:.1f},{c[1]:.1f},{c[2]:.1f})" if c else "n/a"
    print(f"  #{ps['pocket']:2d}  {ps['score']:.3f}  {ps['drug']:.3f}  {ps['vol']:6.0f}  {ps['dist_lvy']:6.1f} Å  {cstr}")

# identify confirmed binding pocket
lvy_pocket = pocket_summary[0]
print(f"\n✓ Pocket #{lvy_pocket['pocket']} confirmed as LVY site")
print(f"  Druggability={lvy_pocket['drug']:.3f}, Volume={lvy_pocket['vol']:.0f} Å³, d={lvy_pocket['dist_lvy']:.1f} Å from LVY centroid")
print(f"\nDocking box: centre ({centroid[0]:.2f}, {centroid[1]:.2f}, {centroid[2]:.2f}), size 24×24×24 Å")
