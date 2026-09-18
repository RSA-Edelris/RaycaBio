
import gemmi, numpy as np

BASE = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/job-6567207/ternary_out"
bridge_res = {98, 100, 134, 135, 136, 137, 138, 139, 154, 190, 191, 192}

def get_chain_atoms(model, chain_name):
    for chain in model:
        if chain.name == chain_name:
            return np.array([[a.pos.x, a.pos.y, a.pos.z]
                             for res in chain for a in res])
    return np.array([])

def get_chain_residues(model, chain_name):
    for chain in model:
        if chain.name == chain_name:
            return list(chain)
    return []

for i in range(3):
    st = gemmi.read_structure(f"{BASE}/gspt1_crbn_glue_{i}.pdb")
    m = st[0]
    lig_xyz = get_chain_atoms(m, 'C')

    print(f"Model {i} — ligand distance to crystal bridging residues (our GSPT1 numbering):")
    for res in get_chain_residues(m, 'A'):
        if res.seqid.num not in bridge_res:
            continue
        xyz = np.array([[a.pos.x, a.pos.y, a.pos.z] for a in res])
        d = float(np.sqrt(((lig_xyz[:, None, :] - xyz[None, :, :])**2).sum(-1)).min())
        flag = " *** CONTACT" if d < 4.5 else ""
        print(f"  {res.name}{res.seqid.num}: {d:.1f} Å{flag}")
    print()
