
# Missing residues, full contact analysis, bridging contacts, waters
import gemmi, numpy as np
from collections import defaultdict

# --- Missing residues: compare entity sequence vs observed ---
st = gemmi.read_structure(cif_path)
model = st[0]

print("=== MISSING RESIDUES ===")
for entity in st.entities:
    if entity.entity_type == gemmi.EntityType.Polymer:
        poly_seq = entity.full_sequence   # one-letter codes
        # Find subchains matching this entity
        for chain in model:
            sub = chain.get_subchain(chain.name)
            # get observed seqids
            obs_seqids = set()
            for res in chain:
                if res.entity_type == gemmi.EntityType.Polymer:
                    obs_seqids.add(res.seqid.num)
            if not obs_seqids:
                continue
            min_s, max_s = min(obs_seqids), max(obs_seqids)
            missing = [s for s in range(min_s, max_s+1) if s not in obs_seqids]
            if missing:
                print(f"  Chain {chain.name}: missing {len(missing)} residues in range {min_s}-{max_s}: {missing[:20]}{'...' if len(missing)>20 else ''}")
            else:
                print(f"  Chain {chain.name}: no missing residues in observed range {min_s}-{max_s}")

# --- Full contact analysis: 85C vs CRBN (chain Z) and GSPT1 (chain X) ---
print("\n=== 85C LIGAND CONTACTS ===")
# Get both copies; use chain Z (CRBN) and chain X (GSPT1)
lig_Z = []
for res in model['Z']:
    if res.name == '85C':
        for atom in res:
            lig_Z.append({'xyz': np.array([atom.pos.x, atom.pos.y, atom.pos.z]),
                          'name': atom.name, 'bfac': atom.b_iso})

lig_xyz = np.array([a['xyz'] for a in lig_Z])
print(f"Ligand atoms: {len(lig_Z)}, B-factor range: {min(a['bfac'] for a in lig_Z):.0f}–{max(a['bfac'] for a in lig_Z):.0f} Å²")
# Flag high-B atoms
high_b = [a['name'] for a in lig_Z if a['bfac'] > 150]
low_b  = [a['name'] for a in lig_Z if a['bfac'] < 80]
print(f"  High B (>150 Å²): {high_b}")
print(f"  Low  B (<80 Å²):  {low_b}")

# --- CRBN contacts ---
def get_res_contacts(chain, lig_xyz, cutoff=4.5):
    contacts = []
    for res in chain:
        if res.entity_type != gemmi.EntityType.Polymer:
            continue
        heavy = []
        for atom in res:
            if atom.element.atomic_number > 1:  # non-H
                heavy.append(np.array([atom.pos.x, atom.pos.y, atom.pos.z]))
        if not heavy:
            continue
        heavy_xyz = np.array(heavy)
        dmat = np.sqrt(((lig_xyz[:, None, :] - heavy_xyz[None, :, :])**2).sum(-1))
        min_d = float(dmat.min())
        if min_d < cutoff:
            contacts.append({'seqid': res.seqid.num, 'resname': res.name, 'min_d': round(min_d, 2)})
    return contacts

crbn_contacts = get_res_contacts(model['Z'], lig_xyz)
gspt1_contacts = get_res_contacts(model['X'], lig_xyz)

print(f"\nCRBN (chain Z) contacts ≤4.5 Å: {len(crbn_contacts)}")
for c in crbn_contacts:
    print(f"  {c['resname']:3s}{c['seqid']:4d}  {c['min_d']:.2f} Å")

print(f"\nGSPT1 (chain X) contacts ≤4.5 Å: {len(gspt1_contacts)}")
for c in gspt1_contacts:
    print(f"  {c['resname']:3s}{c['seqid']:4d}  {c['min_d']:.2f} Å")
