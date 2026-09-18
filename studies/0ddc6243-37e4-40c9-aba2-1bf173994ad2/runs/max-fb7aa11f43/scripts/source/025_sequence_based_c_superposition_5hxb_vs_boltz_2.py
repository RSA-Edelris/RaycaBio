
# Sequence-based Cα superposition: 5HXB vs Boltz-2 predictions
import gemmi, numpy as np
from difflib import SequenceMatcher

BASE = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/job-6567207/ternary_out"

def chain_ca_by_seq(chain):
    """Return list of (one_letter, xyz) for polymer CA atoms."""
    out = []
    for res in chain:
        if res.entity_type != gemmi.EntityType.Polymer:
            continue
        ca = res.find_atom('CA', '\0')
        if ca is None:
            continue
        try:
            aa = gemmi.find_tabulated_residue(res.name).one_letter_code
        except:
            aa = 'X'
        out.append((aa, np.array([ca.pos.x, ca.pos.y, ca.pos.z])))
    return out

def superpose_rmsd(ref_xyz, mob_xyz):
    """Kabsch superposition. Returns RMSD and rotation matrix."""
    ref = np.array(ref_xyz)
    mob = np.array(mob_xyz)
    assert ref.shape == mob.shape
    ref_c = ref.mean(0); mob_c = mob.mean(0)
    A = ref - ref_c; B = mob - mob_c
    H = B.T @ A
    U, S, Vt = np.linalg.svd(H)
    d = np.linalg.det(Vt.T @ U.T)
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    B_rot = (B @ R.T)
    rmsd = np.sqrt(((A - B_rot)**2).sum(-1).mean())
    return rmsd, R, ref_c, mob_c

def sequence_aligned_pairs(seq_ref, seq_mob):
    """Return index pairs where residues match in the longest common alignment."""
    # Use SequenceMatcher on one-letter sequences
    s_ref = ''.join(a for a,_ in seq_ref)
    s_mob = ''.join(a for a,_ in seq_mob)
    sm = SequenceMatcher(None, s_ref, s_mob, autojunk=False)
    ref_idx, mob_idx = [], []
    for block in sm.get_matching_blocks():
        for k in range(block.size):
            ref_idx.append(block.a + k)
            mob_idx.append(block.b + k)
    return ref_idx, mob_idx

# Load 5HXB chains
xhxb_gspt1 = chain_ca_by_seq(model['X'])   # 5HXB GSPT1
xhxb_crbn  = chain_ca_by_seq(model['Z'])   # 5HXB CRBN

print(f"5HXB Chain X (GSPT1): {len(xhxb_gspt1)} CA residues")
print(f"5HXB Chain Z (CRBN):  {len(xhxb_crbn)} CA residues")

# Load Boltz predictions
for i in range(3):
    pred_st = gemmi.read_structure(f"{BASE}/gspt1_crbn_glue_{i}.pdb")[0]
    pred_gspt1 = chain_ca_by_seq(pred_st['A'])
    pred_crbn  = chain_ca_by_seq(pred_st['B'])

    # Align CRBN (use as superposition anchor — larger chain)
    ri_c, mi_c = sequence_aligned_pairs(xhxb_crbn, pred_crbn)
    ref_xyz = [xhxb_crbn[j][1] for j in ri_c]
    mob_xyz = [pred_crbn[j][1] for j in mi_c]
    rmsd_crbn, R, ref_c, mob_c = superpose_rmsd(ref_xyz, mob_xyz)

    # Align GSPT1 independently
    ri_g, mi_g = sequence_aligned_pairs(xhxb_gspt1, pred_gspt1)
    ref_g = [xhxb_gspt1[j][1] for j in ri_g]
    mob_g = [pred_gspt1[j][1] for j in mi_g]
    rmsd_gspt1, _, _, _ = superpose_rmsd(ref_g, mob_g)

    # After superposing on CRBN, compute GSPT1 displacement (interface RMSD proxy)
    # Transform all predicted GSPT1 CA by the CRBN superposition
    mob_g_arr = np.array(mob_g)
    ref_g_arr = np.array(ref_g)
    mob_g_rot = (mob_g_arr - mob_c) @ R.T + ref_c
    crbn_anchored_gspt1_rmsd = np.sqrt(((ref_g_arr - mob_g_rot)**2).sum(-1).mean())

    print(f"\nModel {i} vs 5HXB:")
    print(f"  CRBN superposition: {len(ri_c)} matched CA, RMSD = {rmsd_crbn:.2f} Å")
    print(f"  GSPT1 self-superposition: {len(ri_g)} matched CA, RMSD = {rmsd_gspt1:.2f} Å")
    print(f"  GSPT1 position after CRBN-anchored superposition: RMSD = {crbn_anchored_gspt1_rmsd:.2f} Å")
