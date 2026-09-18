
# Per-model detailed analysis — interface, ligand pocket contacts across all 3 models
import gemmi, numpy as np
from collections import defaultdict

BASE = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/job-6567207/ternary_out"

def parse_pdb_full(path):
    st = gemmi.read_structure(path)
    model = st[0]
    chains = {}
    for chain in model:
        records = []
        for res in chain:
            for atom in res:
                records.append({'xyz': np.array([atom.pos.x, atom.pos.y, atom.pos.z]),
                                 'name': atom.name, 'resname': res.name, 'seqid': res.seqid.num})
        chains[chain.name] = records
    return chains

# Check pLDDT from all 3 CIF files
for i in range(3):
    doc = gemmi.cif.read(f"{BASE}/gspt1_crbn_glue_{i}.cif")
    blk = doc.sole_block()
    vals = [float(v) for v in blk.find_values('_ma_qa_metric_local.metric_value')]
    print(f"Model {i}: _ma_qa_metric_local n={len(vals)}, mean={np.mean(vals):.2f}, unique={sorted(set(vals))}")

print()

# Per-model detailed contacts
for i in range(3):
    ch = parse_pdb_full(f"{BASE}/gspt1_crbn_glue_{i}.pdb")
    
    # CA arrays
    ca_A = np.array([r['xyz'] for r in ch['A'] if r['name'] == 'CA'])
    ca_B = np.array([r['xyz'] for r in ch['B'] if r['name'] == 'CA'])
    lig  = np.array([r['xyz'] for r in ch['C']])
    
    # A-B interface at 8 Å
    d_AB = np.sqrt(((ca_A[:, None, :] - ca_B[None, :, :])**2).sum(-1))
    n_A = int((d_AB < 8.0).any(axis=1).sum())
    n_B = int((d_AB < 8.0).any(axis=0).sum())
    
    # Interface area proxy: count pairs < 8 Å
    n_pairs = int((d_AB < 8.0).sum())
    
    # Min CA-CA
    min_d = float(d_AB.min())
    
    # Ligand - CRBN residue contacts ≤ 4.5 Å
    crbn_by_res = defaultdict(list)
    for r in ch['B']:
        crbn_by_res[r['seqid']].append(r['xyz'])
    
    trp_contacts = []
    for seqid, xyzs in sorted(crbn_by_res.items()):
        xyz_r = np.array(xyzs)
        min_d_lig = float(np.sqrt(((lig[:, None, :] - xyz_r[None, :, :])**2).sum(-1)).min())
        if min_d_lig < 4.5:
            name = next(r['resname'] for r in ch['B'] if r['seqid'] == seqid)
            trp_contacts.append((seqid, name, round(min_d_lig, 2)))
    
    # How many Trp residues contact ligand?
    trp_near = [(s,n,d) for s,n,d in trp_contacts if n == 'TRP']
    
    # Ligand-GSPT1 min dist
    hvy_A = np.array([r['xyz'] for r in ch['A']])
    min_lig_A = float(np.sqrt(((lig[:, None, :] - hvy_A[None, :, :])**2).sum(-1)).min())
    
    print(f"Model {i}:")
    print(f"  A-B: {n_A} GSPT1 res, {n_B} CRBN res in contact; {n_pairs} CA-CA pairs < 8 Å; min CA-CA = {min_d:.2f} Å")
    print(f"  Ligand–CRBN: {len(trp_contacts)} residues within 4.5 Å")
    print(f"  Trp residues near ligand: {trp_near}")
    print(f"  Ligand–GSPT1 min dist: {min_lig_A:.2f} Å")
    print(f"  CRBN pocket residues: {[(s,n) for s,n,_ in trp_contacts]}")
    print()
