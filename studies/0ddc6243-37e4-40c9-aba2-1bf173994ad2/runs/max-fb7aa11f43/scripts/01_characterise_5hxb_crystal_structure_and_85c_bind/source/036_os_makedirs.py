
import gemmi, numpy as np, os

out_dir = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking"
os.makedirs(out_dir, exist_ok=True)

st = gemmi.read_structure(cif_path)

# ---- Receptor: CRBN (Z) + GSPT1 (X), ligand removed, ZN kept ----
st_rec = gemmi.Structure()
st_rec.cell = st.cell
st_rec.spacegroup_hm = st.spacegroup_hm
m_rec = gemmi.Model('1')
for chain in st[0]:
    if chain.name not in ('X', 'Z'):
        continue
    new_chain = gemmi.Chain(chain.name)
    for res in chain:
        if res.name != '85C':
            new_chain.add_residue(res)
    m_rec.add_chain(new_chain)
st_rec.add_model(m_rec)
rec_path = f"{out_dir}/receptor_CRBN_GSPT1.pdb"
st_rec.write_pdb(rec_path)
print(f"Receptor PDB: {rec_path} ({os.path.getsize(rec_path):,} bytes)")

# ---- Ligand 85C reference pose as PDB ----
st_lig = gemmi.Structure()
st_lig.cell = st.cell
m_lig = gemmi.Model('1')
ch_lig = gemmi.Chain('L')
for res in st[0]['Z']:
    if res.name == '85C':
        ch_lig.add_residue(res)
m_lig.add_chain(ch_lig)
st_lig.add_model(m_lig)
lig_pdb = f"{out_dir}/85C_crystal.pdb"
st_lig.write_pdb(lig_pdb)
print(f"Ligand PDB:   {lig_pdb}")

# ---- Docking box centroid ----
centroid = lig_xyz_arr.mean(axis=0)
box_size = 22.0
print(f"\nDocking box:  center=({centroid[0]:.2f}, {centroid[1]:.2f}, {centroid[2]:.2f})")
print(f"              size={box_size} x {box_size} x {box_size} Å")

# ---- Pocket dimensions ----
lig_min = lig_xyz_arr.min(axis=0)
lig_max = lig_xyz_arr.max(axis=0)
lig_span = lig_max - lig_min
print(f"Ligand extent: {lig_span.round(1)} Å (longest {lig_span.max():.1f} Å)")

with open(f"{out_dir}/docking_box.txt", 'w') as f:
    f.write(f"center_x={centroid[0]:.3f}\ncenter_y={centroid[1]:.3f}\ncenter_z={centroid[2]:.3f}\n")
    f.write(f"size_x={box_size}\nsize_y={box_size}\nsize_z={box_size}\n")
print(f"Box params:   {out_dir}/docking_box.txt")
