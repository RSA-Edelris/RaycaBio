#!/usr/bin/env python3
"""
Render an animated GIF of the EL2003A MD trajectory.
Shows: protein Cα backbone (gray), binding-site residues (teal sticks),
ligand heavy atoms (element-colored spheres), RMSD and time labels.
Saves: EL2003A_MD_trajectory.gif  (101 frames, 80 ms/frame ≈ 8 s loop)
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import mdtraj as mdt

WS   = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
WORK = f"{WS}/gbsa_run/EL2003A_pose2"

# ── 1. Load and align trajectory ────────────────────────────────────────────
print("Loading trajectory...")
traj = mdt.load(f"{WORK}/traj_com.xtc", top=f"{WORK}/complex_reres.pdb")
print(f"  {traj.n_frames} frames, {traj.n_atoms} atoms")

# Superpose on Cα of first frame
ca_idx = traj.topology.select("name CA")
traj.superpose(traj[0], atom_indices=ca_idx)
print("  Superposed on Cα (frame 0)")

# ── 2. Compute positional RMSD of ligand over time ──────────────────────────
# Use manual positional RMSD (no re-superposition) because the trajectory is
# already Cα-aligned above. mdt.rmsd() defaults to superpose=True (QCP
# best-fit on ligand atoms), which gives a lower-bound conformational RMSD
# rather than the actual displacement within the binding site.
lig_idx  = traj.topology.select("resname MOL and not element H")
lig_ref  = traj.xyz[0, lig_idx, :]   # reference: frame 0 positions, nm
rmsd_lig = np.sqrt(
    np.mean(np.sum((traj.xyz[:, lig_idx, :] - lig_ref)**2, axis=2), axis=1)
) * 10.0  # nm → Å
print(f"  Ligand positional RMSD range: {rmsd_lig.min():.2f}–{rmsd_lig.max():.2f} Å")

# ── 3. Identify binding-site residues (≤5 Å from ligand at frame 0) ─────────
lig_pos_f0  = traj.xyz[0, lig_idx, :]       # (n_lig, 3) nm
pro_idx_all = traj.topology.select("protein and not element H")
pro_pos_f0  = traj.xyz[0, pro_idx_all, :]  # (n_pro, 3) nm

# Brute-force nearest neighbours within 0.5 nm
diffs = pro_pos_f0[:, None, :] - lig_pos_f0[None, :, :]  # (n_pro, n_lig, 3)
dists = np.sqrt((diffs**2).sum(axis=2))                   # (n_pro, n_lig)
min_dist = dists.min(axis=1)                              # (n_pro,)
site_mask = min_dist < 0.5                                # 5 Å
site_pro_local = pro_idx_all[site_mask]

# Get unique residue indices for binding site
site_res_idx = sorted({traj.topology.atom(a).residue.index
                       for a in site_pro_local})
print(f"  Binding-site residues within 5 Å: {len(site_res_idx)}")

# Atom selection for binding site (heavy atoms)
site_atom_idx = np.array([a.index for a in traj.topology.atoms
                          if a.residue.index in site_res_idx
                          and a.element.symbol != 'H'])

# ── 4. Element colour map ────────────────────────────────────────────────────
ELEM_COLOR = {'C': '#5a5a5a', 'N': '#4e8bca', 'O': '#d95f5f',
              'S': '#e6c42a', 'P': '#f0a000', 'F': '#3ccea0',
              'Cl': '#3ccea0', 'H': '#dddddd'}

def elem_colors(atom_idx_list):
    return [ELEM_COLOR.get(traj.topology.atom(a).element.symbol, '#aaaaaa')
            for a in atom_idx_list]

lig_colors  = elem_colors(lig_idx)
site_colors = elem_colors(site_atom_idx)

# ── 5. Build figure ──────────────────────────────────────────────────────────
DARK_BG = '#0d1117'
plt.style.use('dark_background')
fig = plt.figure(figsize=(7, 7), facecolor=DARK_BG)
ax  = fig.add_subplot(111, projection='3d', facecolor=DARK_BG)

# Compute axis limits from frame 0 binding site
site_xyz0 = traj.xyz[0, site_atom_idx, :] * 10  # Å
centroid   = site_xyz0.mean(axis=0)
span = 20.0  # Å half-width of view box

ax.set_xlim(centroid[0]-span, centroid[0]+span)
ax.set_ylim(centroid[1]-span, centroid[1]+span)
ax.set_zlim(centroid[2]-span, centroid[2]+span)
ax.set_xlabel('X (Å)', color='#666', fontsize=7)
ax.set_ylabel('Y (Å)', color='#666', fontsize=7)
ax.set_zlabel('Z (Å)', color='#666', fontsize=7)
ax.tick_params(colors='#444', labelsize=6)
for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
    pane.fill = False
    pane.set_edgecolor('#1a1a1a')
ax.grid(True, color='#1a1a1a', linewidth=0.4)

# Title / labels
title_txt   = ax.set_title('EL2003A · PDK1 (1Z5M) · MD trajectory',
                           color='white', fontsize=11, pad=8)
time_txt    = ax.text2D(0.02, 0.96, '', transform=ax.transAxes,
                        color='#aaaaaa', fontsize=9)
rmsd_txt    = ax.text2D(0.02, 0.92, '', transform=ax.transAxes,
                        color='#5bc8af', fontsize=9)

# Legend patches (drawn once)
from matplotlib.lines import Line2D
legend_elems = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#5a5a5a',
           markersize=7, label='Ligand C', linestyle='None'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#4e8bca',
           markersize=7, label='Ligand N', linestyle='None'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#d95f5f',
           markersize=7, label='Ligand O', linestyle='None'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='#404040',
           markersize=6, label='Binding site', linestyle='None', alpha=0.5),
    Line2D([0], [0], color='#334455', linewidth=1, label='Backbone Cα'),
]
ax.legend(handles=legend_elems, loc='upper right', fontsize=7,
          facecolor='#111111', edgecolor='#333333', labelcolor='#cccccc')

# ── 6. Draw Cα backbone (static — aligned to first frame, changes every frame) ─
# We redraw per-frame, so just initialise empty artists
ca_lines  = [ax.plot([], [], [], color='#334455', linewidth=0.6, alpha=0.5)[0]]
site_sc   = ax.scatter([], [], [], c=[], s=12, alpha=0.35, depthshade=False)
lig_sc    = ax.scatter([], [], [], c=[], s=60, alpha=0.95, depthshade=True,
                       edgecolors='white', linewidths=0.3)

# Build Cα chain segments (connected backbone)
ca_res = sorted({traj.topology.atom(a).residue.index for a in ca_idx})

def get_ca_xyz(frame_idx):
    """Returns list of (x,y,z) arrays per chain segment."""
    xyz_A = traj.xyz[frame_idx, ca_idx, :] * 10
    return xyz_A

# ── 7. Animate ───────────────────────────────────────────────────────────────
def update(frame_idx):
    xyz = traj.xyz[frame_idx]  # (n_atoms, 3) nm
    t   = traj.time[frame_idx]

    # Backbone Cα
    ca_xyz = xyz[ca_idx] * 10  # Å
    ca_lines[0].set_data(ca_xyz[:, 0], ca_xyz[:, 1])
    ca_lines[0].set_3d_properties(ca_xyz[:, 2])

    # Binding site
    s_xyz = xyz[site_atom_idx] * 10
    site_sc._offsets3d = (s_xyz[:, 0], s_xyz[:, 1], s_xyz[:, 2])
    site_sc.set_color(site_colors)

    # Ligand
    l_xyz = xyz[lig_idx] * 10
    lig_sc._offsets3d = (l_xyz[:, 0], l_xyz[:, 1], l_xyz[:, 2])
    lig_sc.set_color(lig_colors)

    # Labels
    time_txt.set_text(f't = {t:.0f} ps')
    rmsd_txt.set_text(f'Ligand RMSD = {rmsd_lig[frame_idx]:.2f} Å')

    return ca_lines[0], site_sc, lig_sc, time_txt, rmsd_txt

print("Rendering animation (101 frames)...")
ani = animation.FuncAnimation(
    fig, update,
    frames=traj.n_frames,
    interval=80,  # ms per frame
    blit=False,
)

out_gif = f"{WS}/EL2003A_MD_trajectory.gif"
ani.save(out_gif, writer='pillow', fps=12, dpi=110)
print(f"Saved: {out_gif}")

# Also save a static PNG of the final frame
update(traj.n_frames - 1)
out_png = f"{WS}/EL2003A_MD_final_frame.png"
plt.savefig(out_png, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
print(f"Saved: {out_png}")

# ── 8. RMSD plot ─────────────────────────────────────────────────────────────
plt.figure(figsize=(7, 3), facecolor=DARK_BG)
ax2 = plt.gca()
ax2.set_facecolor(DARK_BG)
ax2.plot(traj.time, rmsd_lig, color='#5bc8af', linewidth=1.5)
ax2.axvline(100, color='#aaaaaa', linewidth=0.8, linestyle='--', label='eq cutoff')
ax2.set_xlabel('Time (ps)', color='white', fontsize=10)
ax2.set_ylabel('Ligand RMSD (Å)', color='white', fontsize=10)
ax2.set_title('EL2003A ligand RMSD vs. t=0 pose', color='white', fontsize=11)
ax2.tick_params(colors='#aaaaaa')
ax2.spines['bottom'].set_color('#444')
ax2.spines['left'].set_color('#444')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(labelcolor='#cccccc', facecolor='#111', edgecolor='#333', fontsize=9)
plt.tight_layout()
out_rmsd = f"{WS}/EL2003A_MD_ligand_RMSD.png"
plt.savefig(out_rmsd, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
print(f"Saved: {out_rmsd}")

print("\nDone.")
