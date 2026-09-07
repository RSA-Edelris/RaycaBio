
# ── inspect fpocket output structure ─────────────────────────────────────────
print("Top-level keys:", [k for k in fp.keys()])
print("n_pockets:", fp.get("n_pockets"))
print("top_pocket_score:", fp.get("top_pocket_score"))
print("top_pocket_druggability:", fp.get("top_pocket_druggability"))

pockets = fp.get("pockets", [])
print(f"\nPockets list length: {len(pockets)}")
if pockets:
    print("Pocket[0] keys:", list(pockets[0].keys()))
    print("Pocket[0] sample:", {k: pockets[0][k] for k in list(pockets[0].keys())[:10]})
