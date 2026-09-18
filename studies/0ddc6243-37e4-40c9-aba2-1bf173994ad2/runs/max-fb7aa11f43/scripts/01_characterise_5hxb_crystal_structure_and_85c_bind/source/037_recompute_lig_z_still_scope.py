
import numpy as np, os

# Recompute from lig_Z (still in scope)
lig_xyz_arr = np.array([a['xyz'] for a in lig_Z])
centroid = lig_xyz_arr.mean(axis=0)
box_size  = 22.0

lig_span = lig_xyz_arr.max(0) - lig_xyz_arr.min(0)
print(f"Ligand extent: {lig_span.round(1)} Å  (longest {lig_span.max():.1f} Å)")
print(f"Docking box:  center=({centroid[0]:.3f}, {centroid[1]:.3f}, {centroid[2]:.3f})  size={box_size} Å³")

out_dir = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking"
with open(f"{out_dir}/docking_box.txt", 'w') as f:
    f.write(f"center_x={centroid[0]:.3f}\ncenter_y={centroid[1]:.3f}\ncenter_z={centroid[2]:.3f}\n")
    f.write(f"size_x={box_size}\nsize_y={box_size}\nsize_z={box_size}\n")

# Write protonation notes as a documented file
prot_notes = """\
=== RECEPTOR PREPARATION CHOICES ===

Structure: 5HXB chain Z (CRBN, 380 res) + chain X (GSPT1, 195 res)
Chains removed: Y, B (DDB1 x2), C, A (second ASU copy)

HISTIDINE PROTONATION (binding site residues, from contact geometry):
  HIS353  — contacts ligand O4 via NE2 at 2.72 Å → ε-protonated (HIE)
  HIS357  — distal (4.43 Å), exposed → δ-protonated (HID) as default
  HIS378  — contacts ligand N2 via backbone O at 2.76 Å; side-chain role unclear
              → δ-protonated (HID) to avoid steric conflict
  All other HIS → HID (default) unless buried salt-bridge evident

ZN ION (seqid 501 in chain Z):
  Kept. CRBN contains a structural Zn²⁺ coordinating C173/C176/H228/H230
  (canonical numbering). Remove from docking receptor only if force field
  lacks Zn parameters; include in MD with AMBER Zn parameters (tetra-coord).

WATERS:
  None present in 5HXB at 3.6 Å — none to keep or discard.

DOCKING SITE DEFINITION:
  Centred on 85C geometric centroid in chain Z.
  Box: 22 × 22 × 22 Å (covers full pocket + GSPT1 neo-interface surface).
  Rationale: 85C longest axis = {span:.1f} Å; 22 Å adds ~4 Å buffer on each side.
  Restricted to stabiliser site, not the full CRBN–GSPT1 interface.

LIGAND PREPARATION:
  Reference: 85C extracted from chain Z (crystal pose).
  Input SDF compounds: protonated as-supplied; GNINA adds Gasteiger charges.
  Tautomers: glutarimide NH → keto form enforced (consistent with crystal).
  Boc groups on Compounds 1 and 4 treated as-is (note: may need deprotection
  for cell-active compounds — these likely represent synthetic intermediates).
""".format(span=lig_span.max())

with open(f"{out_dir}/receptor_prep_choices.txt", 'w') as f:
    f.write(prot_notes)
print("Receptor prep notes written.")
print(prot_notes)
