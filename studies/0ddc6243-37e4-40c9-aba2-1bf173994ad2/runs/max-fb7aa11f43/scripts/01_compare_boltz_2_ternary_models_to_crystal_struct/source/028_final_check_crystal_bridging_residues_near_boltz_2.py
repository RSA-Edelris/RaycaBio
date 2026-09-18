
# Final check: are the crystal bridging residues near the Boltz-2 interface?
import gemmi, numpy as np

BASE = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/job-6567207/ternary_out"

# Crystal bridging residues in our GSPT1 numbering
bridge_res = {98, 100, 134, 135, 136, 137, 138, 139, 154, 190, 191, 192}

# For each model: where is the ligand relative to these specific residues?
for i in range(3):
    st = gemmi.read_structure(f"{BASE}/gspt1_crbn_glue_{i}.pdb")[0]
    lig_xyz = np.array([[a.pos.x, a.pos.y, a.pos.z]
                        for res in st[0]['C'] for a in res])

    # Per-residue distance from ligand for the bridging residues
    gspt1_bridge_dists = {}
    for res in st[0]['A']:
        if res.seqid.num not in bridge_res:
            continue
        xyz = np.array([[a.pos.x, a.pos.y, a.pos.z] for a in res])
        d = float(np.sqrt(((lig_xyz[:, None, :] - xyz[None, :, :])**2).sum(-1)).min())
        gspt1_bridge_dists[res.seqid.num] = (res.name, round(d, 1))

    print(f"Model {i} — ligand distance to crystal bridging residues:")
    for rnum in sorted(gspt1_bridge_dists):
        rname, d = gspt1_bridge_dists[rnum]
        flag = " *** CONTACT" if d < 4.5 else ""
        print(f"  res {rnum:3d} ({rname}): {d:.1f} Å{flag}")
    print()
