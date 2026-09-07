
# ── fpocket ───────────────────────────────────────────────────────────────────
with open(receptor_noh_path) as f:
    receptor_content = f.read()

print(f"Sending {len(receptor_content):,} chars to fpocket ...")
fp = dispatch('fpocket', {'structure_content': receptor_content})
print("fpocket rc:", fp.get('rc'))
print("Pockets found:", fp.get('n_pockets'))
print("Top pocket score:", fp.get('top_pocket_score'))
print("Top pocket druggability:", fp.get('top_pocket_druggability'))

# Show top-5 pockets
pockets = fp.get('pockets', [])
print(f"\nTop-5 pockets (of {len(pockets)}):")
for p in pockets[:5]:
    print(f"  Pocket {p.get('rank','?'):>2}: score={p.get('score',0):.2f}  "
          f"drugg={p.get('druggability_score',0):.2f}  "
          f"vol={p.get('volume',0):.0f}Å³  "
          f"center=({p.get('x_centroid',0):.1f},{p.get('y_centroid',0):.1f},{p.get('z_centroid',0):.1f})")
