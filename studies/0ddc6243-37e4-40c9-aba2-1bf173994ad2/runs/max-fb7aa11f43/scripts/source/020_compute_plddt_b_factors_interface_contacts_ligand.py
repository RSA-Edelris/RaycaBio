
# Compute pLDDT from B-factors, interface contacts, ligand contacts, inter-model RMSD
# (functions dropped between calls – redefine here)

import gemmi, numpy as np

BASE = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/job-6567207/ternary_out"

def parse_pdb_full(path):
    st = gemmi.read_structure(path)
    model = st[0]
    chains = {}
    for chain in model:
        records = []
        for res in chain:
            for atom in res:
                records.append({
                    'xyz': np.array([atom.pos.x, atom.pos.y, atom.pos.z]),
                    'bfactor': atom.b_iso,
                    'name': atom.name,
                    'resname': res.name,
                    'seqid': res.seqid.num,
                })
        chains[chain.name] = records
    return chains

def ca_xyz(records):
    return np.array([r['xyz'] for r in records if r['name'] == 'CA'])

def ca_bfac(records):
    return np.array([r['bfactor'] for r in records if r['name'] == 'CA'])

def heavy_xyz(records):
    return np.array([r['xyz'] for r in records])

def count_contacts(xyz_a, xyz_b, cutoff):
    """Count unique residue pairs within cutoff Å (using first heavy atom per residue via CA)."""
    if len(xyz_a) == 0 or len(xyz_b) == 0:
        return 0, 0.0
    # pairwise distances
    diff = xyz_a[:, None, :] - xyz_b[None, :, :]
    dists = np.sqrt((diff**2).sum(-1))
    n_contacts = int((dists < cutoff).any(axis=1).sum()), float(dists.min())
    return n_contacts

all_data = []
for i in range(3):
    ch = parse_pdb_full(f"{BASE}/gspt1_crbn_glue_{i}.pdb")
    
    ca_A = ca_xyz(ch['A']); bf_A = ca_bfac(ch['A'])
    ca_B = ca_xyz(ch['B']); bf_B = ca_bfac(ch['B'])
    lig  = heavy_xyz(ch['C'])

    # pLDDT (B-factor stores per-residue confidence in Boltz outputs)
    plddt_A = bf_A.mean()
    plddt_B = bf_B.mean()
    # pLDDT high/med/low breakdown
    plddt_all = np.concatenate([bf_A, bf_B])
    pct_high  = (plddt_all >= 70).mean() * 100
    pct_vhigh = (plddt_all >= 90).mean() * 100

    # A-B interface: CA-CA ≤ 8 Å
    ab_contacts_A, ab_min = count_contacts(ca_A, ca_B, 8.0)
    _, _ = ab_min, ab_contacts_A  # unpack

    # Also: how many CRBN residues within 8 Å of ANY GSPT1 CA
    diff_AB = ca_A[:, None, :] - ca_B[None, :, :]
    dist_AB = np.sqrt((diff_AB**2).sum(-1))
    n_GSPT1_interface = int((dist_AB < 8.0).any(axis=1).sum())
    n_CRBN_interface  = int((dist_AB < 8.0).any(axis=0).sum())
    min_CA_AB = float(dist_AB.min())

    # Ligand contacts: heavy atoms ≤ 4 Å of any protein heavy atom
    hvy_A = heavy_xyz(ch['A'])
    hvy_B = heavy_xyz(ch['B'])

    diff_LA = lig[:, None, :] - hvy_A[None, :, :]
    dist_LA = np.sqrt((diff_LA**2).sum(-1))
    n_lig_A = int((dist_LA < 4.0).any(axis=0).sum())  # protein atoms near lig
    min_lig_A = float(dist_LA.min())

    diff_LB = lig[:, None, :] - hvy_B[None, :, :]
    dist_LB = np.sqrt((diff_LB**2).sum(-1))
    n_lig_B = int((dist_LB < 4.0).any(axis=0).sum())
    min_lig_B = float(dist_LB.min())

    all_data.append({
        'model': i,
        'plddt_GSPT1': plddt_A, 'plddt_CRBN': plddt_B,
        'plddt_pct_high': pct_high, 'plddt_pct_vhigh': pct_vhigh,
        'n_GSPT1_interface_res': n_GSPT1_interface,
        'n_CRBN_interface_res': n_CRBN_interface,
        'min_CA_AB_ang': min_CA_AB,
        'n_GSPT1_atoms_near_lig': n_lig_A,
        'n_CRBN_atoms_near_lig': n_lig_B,
        'min_lig_GSPT1_ang': min_lig_A,
        'min_lig_CRBN_ang': min_lig_B,
        'ca_A': ca_A, 'ca_B': ca_B, 'lig': lig,
    })
    print(f"Model {i}: pLDDT A={plddt_A:.1f} B={plddt_B:.1f} | "
          f"A-B interface: {n_GSPT1_interface}/{len(ca_A)} GSPT1, {n_CRBN_interface}/{len(ca_B)} CRBN residues (min CA-CA {min_CA_AB:.1f} Å) | "
          f"Lig-GSPT1 {n_lig_A} atoms {min_lig_A:.2f} Å | "
          f"Lig-CRBN {n_lig_B} atoms {min_lig_B:.2f} Å")

# Inter-model Cα RMSD (chain A+B concatenated)
print("\n--- Inter-model Cα RMSD ---")
for i in range(3):
    for j in range(i+1, 3):
        ca_i = np.concatenate([all_data[i]['ca_A'], all_data[i]['ca_B']])
        ca_j = np.concatenate([all_data[j]['ca_A'], all_data[j]['ca_B']])
        rmsd = float(np.sqrt(((ca_i - ca_j)**2).sum(-1).mean()))
        print(f"  Model {i} vs {j}: RMSD = {rmsd:.2f} Å")
