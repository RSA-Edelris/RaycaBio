
# Receptor preparation: extract CRBN+GSPT1, add H, define docking box
# Also compute ligand centroid and pocket dimensions
import gemmi, numpy as np
import os

out_dir = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking"
os.makedirs(out_dir, exist_ok=True)

# ---- 1. Extract ternary receptor (CRBN chain Z + GSPT1 chain X) as PDB ----
st = gemmi.read_structure(cif_path)
st2 = gemmi.Structure()
st2.cell = st.cell
st2.spacegroup_hm = st.spacegroup_hm
m2 = gemmi.Model('1')

for chain in st[0]:
    if chain.name in ('X', 'Z'):   # GSPT1 + CRBN (with ZN and 85C)
        m2.add_chain(chain)

st2.add_model(m2)
st2.update_mmcif_block(gemmi.cif.Block('receptor'))

# Write receptor WITHOUT ligand (for docking)
st3 = gemmi.Structure()
st3.cell = st.cell
m3 = gemmi.Model('1')
for chain in st[0]:
    if chain.name not in ('X', 'Z'):
        continue
    new_chain = gemmi.Chain(chain.name)
    for res in chain:
        if res.name not in ('85C',):   # remove ligand, keep ZN and protein
            new_chain.add_residue(res)
    m3.add_chain(new_chain)
st3.add_model(m3)
rec_path = f"{out_dir}/receptor_CRBN_GSPT1.pdb"
st3[0].write_pdb(rec_path)
print(f"Receptor PDB written: {rec_path} ({os.path.getsize(rec_path):,} bytes)")

# ---- 2. Write ligand 85C as SDF for reference ----
# Extract 85C coordinates from chain Z
lig_85c_path = f"{out_dir}/85C_crystal.pdb"
st4 = gemmi.Structure()
st4.cell = st.cell
m4 = gemmi.Model('1')
ch4 = gemmi.Chain('L')
for res in st[0]['Z']:
    if res.name == '85C':
        ch4.add_residue(res)
m4.add_chain(ch4)
st4.add_model(m4)
st4[0].write_pdb(lig_85c_path)
print(f"Ligand PDB written: {lig_85c_path}")

# ---- 3. Docking box: centroid of 85C + 22 Å box ----
lig_xyz_arr = np.array([a['xyz'] for a in lig_Z])
centroid = lig_xyz_arr.mean(axis=0)
box_size = 22.0   # Å — covers the full pocket plus space for GSPT1 interface
print(f"\nDocking box centroid: {centroid.round(2)}")
print(f"Box size: {box_size} x {box_size} x {box_size} Å")
print(f"boxX={centroid[0]:.3f} boxY={centroid[1]:.3f} boxZ={centroid[2]:.3f}")
print(f"box_sizeX={box_size} box_sizeY={box_size} box_sizeZ={box_size}")

# ---- 4. Pocket dimensions from ligand extent ----
lig_min = lig_xyz_arr.min(axis=0)
lig_max = lig_xyz_arr.max(axis=0)
lig_span = lig_max - lig_min
print(f"\nLigand spatial extent: {lig_span.round(1)} Å  ({lig_span.max():.1f} Å longest axis)")
print(f"Pocket range: X={lig_min[0]:.1f}–{lig_max[0]:.1f}  Y={lig_min[1]:.1f}–{lig_max[1]:.1f}  Z={lig_min[2]:.1f}–{lig_max[2]:.1f}")

# Save box params
with open(f"{out_dir}/docking_box.txt", 'w') as f:
    f.write(f"center_x={centroid[0]:.3f}\ncenter_y={centroid[1]:.3f}\ncenter_z={centroid[2]:.3f}\n")
    f.write(f"size_x={box_size}\nsize_y={box_size}\nsize_z={box_size}\n")
print(f"\nBox params saved: {out_dir}/docking_box.txt")
