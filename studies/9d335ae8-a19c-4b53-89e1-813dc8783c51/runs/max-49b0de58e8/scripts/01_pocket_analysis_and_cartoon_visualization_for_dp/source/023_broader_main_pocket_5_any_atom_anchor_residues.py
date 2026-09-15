
# ── Broader main-pocket: 5 Å from any atom of anchor residues ────────────────
anchor_atoms = [a for a in cdk2 if a['resseq'] in ANCHOR_RES]
anchor_tree  = cKDTree([[a['x'],a['y'],a['z']] for a in anchor_atoms])

main_res_full = {}
for a in cdk2:
    d,_ = anchor_tree.query([a['x'],a['y'],a['z']])
    if d <= 5.0:
        main_res_full[(a['resseq'], a['resname'])] = True

print("=== MAIN POCKET — full shell (≤5 Å of anchor atoms) ===")
for (rseq,rname) in sorted(main_res_full):
    print(f"  {rname:3s} {rseq}")

# Check whether canonical hinge residues are covered
for rseq in [33, 79, 80, 81, 82, 83, 84, 85, 86]:
    found = any(k[0]==rseq for k in main_res_full)
    print(f"  res {rseq} included: {found}")
