
# ── Main pocket: anchor on canonical CDK2 key residues, 6 Å shell ─────────
# Known ATP-binding residues in CDK2 (confirmed in this structure)
ANCHOR_RES = {33, 51, 80, 81, 83, 84, 127, 145, 146, 147, 177}  # K33 E51 F80 E81 L83 H84 D127 D145 F146 G147 C177

cdk2_coords  = np.array([[a['x'],a['y'],a['z']] for a in cdk2])
cdk2_resseqs = np.array([a['resseq'] for a in cdk2])

# Centroid of anchor Cα positions
anchor_ca = np.array([[a['x'],a['y'],a['z']] for a in cdk2
                       if a['name']=='CA' and a['resseq'] in ANCHOR_RES])
atp_centroid = anchor_ca.mean(axis=0)
print(f"ATP centroid: {atp_centroid}")

# All CDK2 residues within 6 Å of ATP centroid
main_res_cdk2 = {}
for a in cdk2:
    d = np.linalg.norm(np.array([a['x'],a['y'],a['z']]) - atp_centroid)
    if d <= 6.0:
        main_res_cdk2[(a['resseq'], a['resname'])] = True

print(f"\n=== MAIN POCKET (CDK2 chain A, ≤6 Å of ATP centroid) ===")
for (rseq,rname) in sorted(main_res_cdk2):
    print(f"  {rname:3s} {rseq}")

# ── Allosteric pocket: Cluster 4 (T-loop, residues identified above) ─────────
ALLO_RES_CDK2 = {156,157,158,159,161,163,172,173,174,175,176,177,178,179,180,181}

print(f"\n=== ALLOSTERIC POCKET (T-loop / C-lobe activation loop, Cluster 4) ===")
allo_check = {}
for a in cdk2:
    if a['resseq'] in ALLO_RES_CDK2:
        allo_check[(a['resseq'],a['resname'])] = True
for (rseq,rname) in sorted(allo_check):
    print(f"  {rname:3s} {rseq}")

# ── CDK2-CCNE1 interface pocket: Cluster 14 ──────────────────────────────────
IFACE_CDK2  = {116,119,120,121,122}
IFACE_CCNE1 = {90,95,96,97,98,99,100,101,102,103,104,105}
print(f"\n=== CDK2-CCNE1 INTERFACE (Cluster 14) ===")
print(f"  CDK2  residues: {sorted(IFACE_CDK2)}")
print(f"  CCNE1 residues: {sorted(IFACE_CCNE1)}")
