
import biotite.structure as struc
import biotite.structure.io.pdb as bpdb

pdb_file = bpdb.PDBFile.read(PDB)
structure = bpdb.get_structure(pdb_file, model=1)
prot_mask = struc.filter_amino_acids(structure)
prot_full = structure[prot_mask]

# Separate chains
cdk2_s  = prot_full[prot_full.chain_id == 'A']
ccne1_s = prot_full[prot_full.chain_id == 'B']

# Secondary structure (P-SEA)
sse_cdk2  = struc.annotate_sse(cdk2_s)
sse_ccne1 = struc.annotate_sse(ccne1_s)

# Cα for each chain
ca_cdk2  = cdk2_s[cdk2_s.atom_name == 'CA']
ca_ccne1 = ccne1_s[ccne1_s.atom_name == 'CA']

print(f"CDK2  Cα: {len(ca_cdk2)},  SSE: {len(sse_cdk2)}")
print(f"CCNE1 Cα: {len(ca_ccne1)}, SSE: {len(sse_ccne1)}")

# Combined Cα for PCA
all_ca = np.vstack([ca_cdk2.coord, ca_ccne1.coord])
mu_ = all_ca.mean(axis=0)
_, _, Vt = np.linalg.svd(all_ca - mu_)
V1, V2, V3 = Vt[0], Vt[1], Vt[2]

def proj2d(xyz):
    c = np.atleast_2d(xyz) - mu_
    return c @ V1, c @ V3

# Check pocket separations in this view
MAIN_FINAL  = {15,17,18,33,51,64,79,80,81,83,84,127,132,145,146,147,177}
ALLO_FINAL  = {156,157,158,159,161,163,172,173,174,175,176,177,178,179,180,181}
IFACE_FINAL = {116,119,120,121,122}  # CDK2 side of interface

main_ca  = [a for a in cdk2  if a['name']=='CA' and a['resseq'] in MAIN_FINAL]
allo_ca  = [a for a in cdk2  if a['name']=='CA' and a['resseq'] in ALLO_FINAL]
iface_ca = [a for a in cdk2  if a['name']=='CA' and a['resseq'] in IFACE_FINAL]
# CyclinE1 interface side
iface_ccne1_ca = [a for a in ccne1 if a['name']=='CA' and a['resseq'] in IFACE_CCNE1]

# Centroids
def cen(lst): return np.mean([[a['x'],a['y'],a['z']] for a in lst],axis=0)
main_cen  = cen(main_ca)
allo_cen  = cen(allo_ca)
iface_cen = cen(iface_ca)

for name, c in [('Main ATP', main_cen), ('Allosteric T-loop', allo_cen), ('CDK2-CCNE1 interface', iface_cen)]:
    px, py = proj2d(c)
    print(f"{name}: proj=({float(px):.1f},{float(py):.1f})")
print(f"Main–Allo dist: {np.linalg.norm(main_cen-allo_cen):.1f} Å")
print(f"Main–Iface dist: {np.linalg.norm(main_cen-iface_cen):.1f} Å")
