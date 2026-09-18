
# Map 5HXB GSPT1 seqids → our Boltz-2 residue numbers
# Then compute CRBN TBD-only RMSD and ligand RMSD
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

def superpose_rmsd_Kabsch(ref_xyz, mob_xyz):
    ref = np.array(ref_xyz); mob = np.array(mob_xyz)
    rc = ref.mean(0); mc = mob.mean(0)
    H = (mob - mc).T @ (ref - rc)
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ np.diag([1,1,np.linalg.det(Vt.T @ U.T)]) @ U.T
    mob_rot = (mob - mc) @ R.T + rc
    rmsd = np.sqrt(((ref - mob_rot)**2).sum(-1).mean())
    return rmsd, R, rc, mc, mob_rot

# Build sequence offset: 5HXB chain X seqids vs our GSPT1 1-indexed
xhxb_gspt1_ca = chain_ca_by_seq(model['X'])  # (aa, xyz, seqid)
# Print first 5 to get start seqid
print("5HXB GSPT1 first residues:", [(aa, sid) for aa,_,sid in xhxb_gspt1_ca[:8]])
print("5HXB GSPT1 last residues:", [(aa, sid) for aa,_,sid in xhxb_gspt1_ca[-5:]])

xhxb_crbn_ca = chain_ca_by_seq(model['Z'])
print(f"\n5HXB CRBN seqid range: {xhxb_crbn_ca[0][2]} – {xhxb_crbn_ca[-1][2]}")

# Our GSPT1 input was: GSGPIRLPIVDKYKDMG... (1-indexed)
# 5HXB chain X first residue seqid → this is canonical eRF3a numbering
# Offset = 5HXB_seqid - our_boltz_seqid
# Since 5HXB GSPT1 starts at IRLP and our sequence starts at GSGPIRLP,
# 5HXB first residue (e.g., seqid 533) = our residue ~4 (P at GSGP)
# Offset = 5HXB_seqid_first - 4
first_5hxb_seqid = xhxb_gspt1_ca[0][2]
offset_gspt1 = first_5hxb_seqid - 4   # approximate; will verify with alignment
print(f"\n5HXB GSPT1 first seqid={first_5hxb_seqid}, estimated offset={offset_gspt1}")

# Crystal GSPT1 bridging contacts in our numbering
crystal_bridge = [(534,'GLN',3.71),(536,'VAL',3.07),(570,'VAL',3.67),
                  (571,'ASP',3.70),(572,'LYS',2.66),(573,'LYS',2.93),
                  (574,'SER',2.56),(575,'GLY',3.32),(590,'VAL',3.81),
                  (626,'ILE',3.23),(627,'GLY',3.51),(628,'LYS',2.53)]
print("\nCrystal GSPT1 bridging contacts mapped to our GSPT1 numbering:")
for seqid, rname, dist in crystal_bridge:
    our_res = seqid - offset_gspt1
    print(f"  Crystal {rname}{seqid} → our residue {our_res} ({dist} Å)")

# Now: CRBN thalidomide-binding domain only — last ~120 residues of chain Z
# In 5HXB numbering, TBD is roughly residues 320-406 (canonical) = seqids 320–406 range
# Find residues in 5HXB chain Z with seqid >= 320 (TBD)
xhxb_crbn_tbd = [(aa,xyz,sid) for aa,xyz,sid in xhxb_crbn_ca if sid >= 320]
print(f"\n5HXB CRBN TBD (seqid≥320): {len(xhxb_crbn_tbd)} residues")

# Load pred model 0, get CRBN CA, filter to same seqid range with offset
# Our CRBN offset: our_res + 36 = 5HXB_seqid → our_res = 5HXB_seqid - 36
# TBD in our numbering: seqid >= 320 - 36 = 284
BASE = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/job-6567207/ternary_out"
pred_st0 = gemmi.read_structure(f"{BASE}/gspt1_crbn_glue_0.pdb")[0]
pred_crbn_ca = chain_ca_by_seq(pred_st0['B'])  # seqids 1-406
pred_crbn_tbd = [(aa,xyz,sid) for aa,xyz,sid in pred_crbn_ca if sid >= 284]
print(f"Pred model 0 CRBN TBD (seqid≥284): {len(pred_crbn_tbd)} residues")

# Sequence-align TBD
sm = SequenceMatcher(None,
    ''.join(a for a,_,_ in xhxb_crbn_tbd),
    ''.join(a for a,_,_ in pred_crbn_tbd), autojunk=False)
ri, mi = [], []
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        ri.append(blk.a + k); mi.append(blk.b + k)

ref_xyz = [xhxb_crbn_tbd[j][1] for j in ri]
mob_xyz = [pred_crbn_tbd[j][1] for j in mi]
rmsd_tbd, R_tbd, rc_tbd, mc_tbd, mob_rot_tbd = superpose_rmsd_Kabsch(ref_xyz, mob_xyz)
print(f"\nCRBN TBD superposition: {len(ri)} matched CA, RMSD = {rmsd_tbd:.2f} Å")
