
# ── 1. fpocket with correct key ───────────────────────────────────────────────
fp = run_aidd_tool("fpocket", {"structure": noh_rec_path})
print(f"fpocket rc={fp.get('rc')}  n_pockets={fp.get('n_pockets')}  top_score={fp.get('top_pocket_score'):.3f}  top_drug={fp.get('top_pocket_druggability'):.3f}")

pockets = fp.get("pockets", [])
best_match, best_d = None, 999
for i, p in enumerate(pockets[:10]):
    cx, cy, cz = p.get("center_x",0), p.get("center_y",0), p.get("center_z",0)
    d = np.linalg.norm(np.array([cx, cy, cz]) - centroid)
    score = p.get("druggability_score", 0)
    vol   = p.get("volume", 0)
    print(f"  #{i+1} score={score:.3f} vol={vol:.0f} Å³  center=({cx:.1f},{cy:.1f},{cz:.1f})  d_LVY={d:.1f} Å")
    if d < best_d:
        best_d = d; best_match = i+1

print(f"\n→ Pocket closest to LVY: #{best_match} at {best_d:.1f} Å from LVY centroid")
print(f"  Box confirmed at LVY centroid: X={centroid[0]:.2f}  Y={centroid[1]:.2f}  Z={centroid[2]:.2f}")
