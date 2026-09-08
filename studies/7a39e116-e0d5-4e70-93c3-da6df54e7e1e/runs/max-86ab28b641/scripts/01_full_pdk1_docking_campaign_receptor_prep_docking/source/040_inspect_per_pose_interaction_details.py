
# Inspect per-pose interaction details
for i, res in enumerate(interaction_results, 1):
    print(f"\nPose {i}:")
    hb = res.get('hbonds', [])
    hp = res.get('hphob', [])
    print(f"  H-bonds ({len(hb)}): {hb}")
    print(f"  Hydrophobic ({len(hp)}): {hp[:10]}")
