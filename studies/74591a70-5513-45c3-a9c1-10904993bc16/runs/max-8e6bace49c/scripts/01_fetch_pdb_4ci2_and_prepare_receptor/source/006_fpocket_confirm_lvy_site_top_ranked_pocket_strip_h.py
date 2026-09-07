
# ── FPOCKET: confirm LVY site is top-ranked pocket ────────────────────────────
# Strip H from receptor first (fpocket alpha-sphere algo works on heavy atoms)
import subprocess, re

noh_rec_path = f"{WORK}/4CI2_receptor_noh.pdb"
with open(rec_path) as fin, open(noh_rec_path, 'w') as fout:
    for line in fin:
        rec = line[:6].strip()
        if rec in ("ATOM","HETATM"):
            aname = line[12:16].strip()
            elem = line[76:78].strip() if len(line) >= 78 else ""
            # skip explicit H / D atoms
            if aname.startswith("H") or aname.startswith("D") or elem in ("H","D"):
                continue
        fout.write(line)
print(f"No-H receptor written: {noh_rec_path}")

fpocket_result = run_aidd_tool("fpocket", {"pdbFile": noh_rec_path})
print(f"fpocket rc={fpocket_result.get('rc')}")
print(f"n_pockets: {fpocket_result.get('n_pockets')}")
print(f"top pocket druggability: {fpocket_result.get('top_pocket_druggability')}")
print(f"top pocket score: {fpocket_result.get('top_pocket_score')}")

# Print top-3 pockets
pockets = fpocket_result.get("pockets", [])
for i, p in enumerate(pockets[:5]):
    cx = p.get("center_x", p.get("cx", "?"))
    cy = p.get("center_y", p.get("cy", "?"))
    cz = p.get("center_z", p.get("cz", "?"))
    score = p.get("druggability_score", p.get("score", "?"))
    vol   = p.get("volume", "?")
    print(f"  Pocket {i+1}: center=({cx:.1f},{cy:.1f},{cz:.1f})  score={score}  vol={vol}")

# Compute distance from each pocket centre to LVY centroid
print(f"\nLVY centroid: {centroid.round(2).tolist()}")
for i, p in enumerate(pockets[:5]):
    cx = p.get("center_x", p.get("cx", 0))
    cy = p.get("center_y", p.get("cy", 0))
    cz = p.get("center_z", p.get("cz", 0))
    d = np.linalg.norm(np.array([cx, cy, cz]) - centroid)
    print(f"  Pocket {i+1} → LVY centroid dist: {d:.1f} Å  score={p.get('druggability_score','?')}")
