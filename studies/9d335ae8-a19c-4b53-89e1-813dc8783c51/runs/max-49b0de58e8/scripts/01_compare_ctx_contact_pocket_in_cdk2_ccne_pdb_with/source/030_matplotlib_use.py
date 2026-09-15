
import sys, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.spatial import cKDTree
import biotite.structure as struc
import biotite.structure.io.pdb as pdb_io

sys.path.insert(0, '/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8')
from cartoon_utils import draw_helix, draw_strand, draw_loop

pdb_path = "/home/ubuntu/rayca-artifacts/5e3a2eab5918b528d391eb88/files/CDK2-CCNE.pdb"
pf = pdb_io.PDBFile.read(pdb_path)
structure = pdb_io.get_structure(pf, model=1)

# Separate chains
cdk2_mask  = (structure.chain_id == 'A') & struc.filter_amino_acids(structure)
ccne1_mask = (structure.chain_id == 'B') & struc.filter_amino_acids(structure)
cdk2_s  = structure[cdk2_mask]
ccne1_s = structure[ccne1_mask]

# SSE
sse_a = struc.annotate_sse(cdk2_s)
sse_b = struc.annotate_sse(ccne1_s)

# Build Cα tables per chain
def ca_table(s, sse):
    ca = s[s.atom_name == 'CA']
    assert len(ca) == len(sse), f"length mismatch {len(ca)} vs {len(sse)}"
    return [(int(ca.res_id[i]), ca.coord[i], sse[i]) for i in range(len(ca))]

ca_a = ca_table(cdk2_s,  sse_a)
ca_b = ca_table(ccne1_s, sse_b)

# PCA on all Cα — use same approach as dpCDK2-CCNE1
all_ca = np.vstack([c[1] for c in ca_a] + [c[1] for c in ca_b])
mean   = all_ca.mean(0)
U, S, Vt = np.linalg.svd(all_ca - mean, full_matrices=False)
pcs = (all_ca - mean) @ Vt.T   # shape (N, 3)
n_a, n_b = len(ca_a), len(ca_b)
pcs_a, pcs_b = pcs[:n_a], pcs[n_a:]

def proj(ca_list, pc_data):
    return [(r, pc_data[i, 0], pc_data[i, 2], pc_data[i, 1]) for i, (r,_,_) in enumerate(ca_list)]

proj_a = proj(ca_a, pcs_a)
proj_b = proj(ca_b, pcs_b)

# Segment runner
def make_segs(proj_list, sse_list):
    segs = []
    cur_type, cur_pts, cur_depths = sse_list[0], [], []
    for i, (r, px, py, pd) in enumerate(proj_list):
        t = sse_list[i]
        if t == cur_type:
            cur_pts.append((px, py)); cur_depths.append(pd)
        else:
            segs.append((cur_type, cur_pts, np.mean(cur_depths)))
            cur_type = t; cur_pts = [(px, py)]; cur_depths = [pd]
    segs.append((cur_type, cur_pts, np.mean(cur_depths)))
    return segs

sse_a_list = [c[2] for c in ca_a]
sse_b_list = [c[2] for c in ca_b]
segs_a = make_segs(proj_a, sse_a_list)
segs_b = make_segs(proj_b, sse_b_list)

print(f"Chains: CDK2 {len(ca_a)} Cα, CyclinE1 {len(ca_b)} Cα")
print(f"Segments A: {len(segs_a)}, B: {len(segs_b)}")
print("PC variance fractions:", (S[:3]**2 / (S**2).sum()).round(3))
