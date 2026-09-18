
# 1. Crystal 5HXB: ligand (85C) contacts with CRBN and GSPT1
# 2. CRBN C-terminal domain (TBD, ~last 120 residues) alignment only
import gemmi, numpy as np
from difflib import SequenceMatcher

def chain_ca_by_seq(chain):
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
        out.append((aa, np.array([ca.pos.x, ca.pos.y, ca.pos.z]), res.seqid.num))
    return out

def superpose_rmsd(ref_xyz, mob_xyz):
    ref = np.array(ref_xyz); mob = np.array(mob_xyz)
    rc = ref.mean(0); mc = mob.mean(0)
    H = (mob - mc).T @ (ref - rc)
    U, S, Vt = np.linalg.svd(H)
    d = np.linalg.det(Vt.T @ U.T)
    R = Vt.T @ np.diag([1,1,d]) @ U.T
    rmsd = np.sqrt((((ref - rc) - (mob - mc) @ R.T)**2).sum(-1).mean())
    return rmsd, R, rc, mc

def sequence_aligned_pairs(seq_ref, seq_mob):
    s_ref = ''.join(a for a,_,_ in seq_ref)
    s_mob = ''.join(a for a,_,_ in seq_mob)
    sm = SequenceMatcher(None, s_ref, s_mob, autojunk=False)
    ri, mi = [], []
    for block in sm.get_matching_blocks():
        for k in range(block.size):
            ri.append(block.a + k); mi.append(block.b + k)
    return ri, mi

# --- 5HXB ligand contacts ---
# Extract 85C ligand from chain Z
lig_atoms = []
for res in model['Z']:
    if res.name == '85C':
        for atom in res:
            lig_atoms.append(np.array([atom.pos.x, atom.pos.y, atom.pos.z]))
lig_xyz = np.array(lig_atoms)
print(f"5HXB ligand (85C) atoms: {len(lig_xyz)}")

# CRBN contacts in 5HXB
crbn_by_res = {}
for res in model['Z']:
    if res.entity_type != gemmi.EntityType.Polymer:
        continue
    atoms_xyz = np.array([[a.pos.x, a.pos.y, a.pos.z] for a in res])
    crbn_by_res[res.seqid.num] = (res.name, atoms_xyz)

crbn_contacts_5hxb = []
for seqid, (rname, rxyz) in sorted(crbn_by_res.items()):
    d = np.sqrt(((lig_xyz[:, None, :] - rxyz[None, :, :])**2).sum(-1)).min()
    if d < 4.5:
        crbn_contacts_5hxb.append((seqid, rname, round(float(d), 2)))

print("\n5HXB CRBN residues within 4.5 Å of 85C:")
print(crbn_contacts_5hxb)
trp_5hxb = [(s,n,d) for s,n,d in crbn_contacts_5hxb if n == 'TRP']
print(f"  Trp contacts: {trp_5hxb}")

# GSPT1 contacts with ligand in 5HXB
gspt1_by_res = {}
for res in model['X']:
    if res.entity_type != gemmi.EntityType.Polymer:
        continue
    atoms_xyz = np.array([[a.pos.x, a.pos.y, a.pos.z] for a in res])
    gspt1_by_res[res.seqid.num] = (res.name, atoms_xyz)

gspt1_contacts_5hxb = []
for seqid, (rname, rxyz) in sorted(gspt1_by_res.items()):
    d = np.sqrt(((lig_xyz[:, None, :] - rxyz[None, :, :])**2).sum(-1)).min()
    if d < 4.5:
        gspt1_contacts_5hxb.append((seqid, rname, round(float(d), 2)))

print(f"\n5HXB GSPT1 residues within 4.5 Å of 85C (bridging contacts):")
print(gspt1_contacts_5hxb)

min_lig_gspt1_5hxb = min(
    np.sqrt(((lig_xyz[:, None, :] - rxyz[None, :, :])**2).sum(-1)).min()
    for _, (_, rxyz) in gspt1_by_res.items()
)
print(f"Min ligand–GSPT1 distance in 5HXB: {min_lig_gspt1_5hxb:.2f} Å")
