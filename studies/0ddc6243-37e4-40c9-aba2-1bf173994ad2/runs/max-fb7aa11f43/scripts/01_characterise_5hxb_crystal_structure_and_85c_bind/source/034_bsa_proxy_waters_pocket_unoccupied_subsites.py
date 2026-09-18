
# BSA proxy, waters, pocket unoccupied subsites
import gemmi, numpy as np
from collections import defaultdict

# --- BSA proxy: count interface Cα pairs and estimate from PISA-style approach ---
# CRBN (chain Z) polymer atoms at interface with GSPT1 (chain X), excluding ligand
crbn_xyz, gspt1_xyz = [], []
for res in model['Z']:
    if res.entity_type == gemmi.EntityType.Polymer:
        for atom in res:
            if atom.element.atomic_number > 1:
                crbn_xyz.append(np.array([atom.pos.x, atom.pos.y, atom.pos.z]))
for res in model['X']:
    if res.entity_type == gemmi.EntityType.Polymer:
        for atom in res:
            if atom.element.atomic_number > 1:
                gspt1_xyz.append(np.array([atom.pos.x, atom.pos.y, atom.pos.z]))

crbn_arr  = np.array(crbn_xyz)
gspt1_arr = np.array(gspt1_xyz)

# Count heavy-atom pairs within 4.5 Å across the interface (proxy for BSA)
# Fast via broadcasting in chunks
n_pairs_45 = 0
for i in range(0, len(crbn_arr), 500):
    chunk = crbn_arr[i:i+500]
    dmat = np.sqrt(((chunk[:, None, :] - gspt1_arr[None, :, :])**2).sum(-1))
    n_pairs_45 += int((dmat < 4.5).sum())
print(f"CRBN–GSPT1 interface heavy-atom pairs <4.5 Å: {n_pairs_45}")
print(f"(BSA estimate ≈ {n_pairs_45 * 4:.0f}–{n_pairs_45 * 6:.0f} Å² — rough proxy)")

# --- Structured waters ---
# Waters in chain Z (HOH) within 3.5 Å of 85C and/or CRBN/GSPT1 interface
lig_xyz = np.array([a['xyz'] for a in lig_Z])

# All HOH from the full structure
waters_near_lig = []
waters_near_interface = []

for chain in model:
    for res in chain:
        if res.name == 'HOH':
            for atom in res:
                w = np.array([atom.pos.x, atom.pos.y, atom.pos.z])
                d_lig = float(np.sqrt(((lig_xyz - w)**2).sum(-1)).min())
                d_crbn = float(np.sqrt(((crbn_arr - w)**2).sum(-1)).min())
                d_gspt = float(np.sqrt(((gspt1_arr - w)**2).sum(-1)).min())
                if d_lig < 3.5:
                    waters_near_lig.append({'chain': chain.name, 'seqid': res.seqid.num,
                                             'd_lig': round(d_lig,2), 'd_crbn': round(d_crbn,2), 'd_gspt': round(d_gspt,2),
                                             'bfac': atom.b_iso})
                elif d_crbn < 4.0 and d_gspt < 4.0:
                    waters_near_interface.append({'chain': chain.name, 'seqid': res.seqid.num,
                                                  'd_lig': round(d_lig,2), 'd_crbn': round(d_crbn,2), 'd_gspt': round(d_gspt,2),
                                                  'bfac': atom.b_iso})

print(f"\nWaters within 3.5 Å of ligand 85C: {len(waters_near_lig)}")
for w in waters_near_lig:
    print(f"  Chain {w['chain']} HOH{w['seqid']}  d_lig={w['d_lig']} d_crbn={w['d_crbn']} d_gspt={w['d_gspt']} B={w['bfac']:.0f}")

print(f"\nInterface bridging waters (≤4Å from both CRBN and GSPT1, not near lig): {len(waters_near_interface)}")
for w in waters_near_interface[:10]:
    print(f"  Chain {w['chain']} HOH{w['seqid']}  d_lig={w['d_lig']} d_crbn={w['d_crbn']} d_gspt={w['d_gspt']} B={w['bfac']:.0f}")

# Total waters in structure
total_hoh = sum(1 for chain in model for res in chain if res.name == 'HOH')
print(f"\nTotal HOH in structure: {total_hoh}")
