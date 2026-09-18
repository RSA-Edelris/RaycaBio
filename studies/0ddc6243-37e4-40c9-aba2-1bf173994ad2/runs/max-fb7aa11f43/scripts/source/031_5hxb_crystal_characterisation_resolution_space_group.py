
# 5HXB crystal characterisation: resolution, space group, missing residues,
# alt conformations, ligand occupancy and B-factors
import gemmi, numpy as np

cif_path = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/5HXB.cif"
doc  = gemmi.cif.read(cif_path)
blk  = doc.sole_block()

# --- Resolution and space group ---
resol = blk.find_value('_reflns.d_resolution_high') or blk.find_value('_refine.ls_d_res_high')
sg    = blk.find_value('_symmetry.space_group_name_H-M') or blk.find_value('_space_group.name_H-M_alt')
cell_a = blk.find_value('_cell.length_a')
cell_b = blk.find_value('_cell.length_b')
cell_c = blk.find_value('_cell.length_c')
cell_alpha = blk.find_value('_cell.angle_alpha')
cell_beta  = blk.find_value('_cell.angle_beta')
cell_gamma = blk.find_value('_cell.angle_gamma')
print(f"Resolution:   {resol} Å")
print(f"Space group:  {sg}")
print(f"Unit cell:    a={cell_a} b={cell_b} c={cell_c} Å | α={cell_alpha} β={cell_beta} γ={cell_gamma}°")

# --- R-factors ---
r_work = blk.find_value('_refine.ls_R_factor_R_work')
r_free = blk.find_value('_refine.ls_R_factor_R_free')
print(f"R_work/R_free: {r_work} / {r_free}")

# --- Ligand (85C) occupancy and B-factors ---
st = gemmi.read_structure(cif_path)
model = st[0]

lig_occ, lig_bfac = [], []
for chain in model:
    for res in chain:
        if res.name == '85C':
            for atom in res:
                lig_occ.append(atom.occ)
                lig_bfac.append(atom.b_iso)

print(f"\n85C occupancy: min={min(lig_occ):.2f} max={max(lig_occ):.2f} mean={np.mean(lig_occ):.2f}")
print(f"85C B-factors: min={min(lig_bfac):.1f} max={max(lig_bfac):.1f} mean={np.mean(lig_bfac):.1f} Å²")

# Surrounding CRBN residues B-factors for comparison
crbn_bfac = []
for res in model['Z']:
    if res.entity_type == gemmi.EntityType.Polymer:
        for atom in res:
            crbn_bfac.append(atom.b_iso)
print(f"CRBN chain B:  mean={np.mean(crbn_bfac):.1f} Å² (context for ligand B)")

# --- Alternate conformations ---
alt_res = []
for chain in model:
    for res in chain:
        alts = set()
        for atom in res:
            if atom.altloc != '\0':
                alts.add(atom.altloc)
        if alts:
            alt_res.append((chain.name, res.seqid.num, res.name, sorted(alts)))
print(f"\nResidues with alternate conformations: {len(alt_res)}")
for c, s, n, a in alt_res[:20]:
    print(f"  Chain {c} {n}{s} alts={a}")
