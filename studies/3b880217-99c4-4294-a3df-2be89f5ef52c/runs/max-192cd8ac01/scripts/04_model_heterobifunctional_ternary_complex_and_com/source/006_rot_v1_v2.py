
import numpy as np, pickle

def rot_v1_to_v2(v1, v2):
    v1=v1/np.linalg.norm(v1); v2=v2/np.linalg.norm(v2)
    cr=np.cross(v1,v2); dt=np.clip(np.dot(v1,v2),-1,1); cn=np.linalg.norm(cr)
    if cn<1e-9:
        if dt>0: return np.eye(3)
        ax=np.cross(v1,[1,0,0] if abs(v1[0])<0.9 else [0,1,0]); ax/=np.linalg.norm(ax)
        return 2*np.outer(ax,ax)-np.eye(3)
    ax=cr/cn; ang=np.arctan2(cn,dt)
    K=np.array([[0,-ax[2],ax[1]],[ax[2],0,-ax[0]],[-ax[1],ax[0],0]])
    return np.eye(3)+np.sin(ang)*K+(1-np.cos(ang))*(K@K)

def rodrigues(ax, angle):
    K=np.array([[0,-ax[2],ax[1]],[ax[2],0,-ax[0]],[-ax[1],ax[0],0]])
    return np.eye(3)+np.sin(angle)*K+(1-np.cos(angle))*(K@K)

with open("geom.pkl","rb") as f: g=pickle.load(f)
u52_com=g["u52_com"]; eam_com=g["eam_com"]
asn140=g["asn140"]; pocket_axis=g["pocket_axis"]
kac_nz_brd4=g["kac_nz_brd4"]; lys_details=g["lys_details"]

# ── BRD4 heavy atoms: split into entrance-side and interior-side ──────────────
brd4_c   = brd4_atoms - kac_nz_brd4   # centred on Kac-Nz anchor

# Project each BRD4 atom along pocket_axis (entrance direction)
# negative projection = interior (away from entrance = toward BCL6 in rotated frame)
brd4_proj    = brd4_c @ pocket_axis    # signed projection along entrance direction
brd4_entrance_mask = brd4_proj > 0    # atoms on entrance side of Kac-Nz (face BCL6 after rotation)
d_brd4_entrance = float(np.linalg.norm(brd4_c[brd4_entrance_mask], axis=1).min()) \
    if brd4_entrance_mask.any() else 999.0
nearest_brd4_entrance_proj = float(brd4_proj[brd4_entrance_mask].max()) \
    if brd4_entrance_mask.any() else 0.0

print("=== BRD4 BD1 entrance-side atoms (face BCL6 after rotation) ===")
print(f"  Nearest BRD4 atom (entrance side) to Kac-Nz anchor: {d_brd4_entrance:.2f} Å")
print(f"  Max entrance projection of these atoms:              {nearest_brd4_entrance_proj:.2f} Å")

# Identify which BRD4 residue carries this nearest entrance atom
brd4_res_atoms = [(res, a) for res in brd4_chain if res.id[0]==' '
                   for a in res.get_atoms() if a.element not in ('H','')]
brd4_coords = np.array([a.coord for res,a in brd4_res_atoms])
brd4_c_all  = brd4_coords - kac_nz_brd4
brd4_proj_all = brd4_c_all @ pocket_axis
# nearest entrance atom
ent_mask = brd4_proj_all > 0
if ent_mask.any():
    dists_ent = np.linalg.norm(brd4_c_all[ent_mask], axis=1)
    idx = np.argwhere(ent_mask).flatten()[np.argmin(dists_ent)]
    res_near, atom_near = brd4_res_atoms[idx]
    print(f"  Nearest entrance-side atom: {res_near.resname}{res_near.id[1]} {atom_near.name} "
          f"  Bfactor={atom_near.bfactor:.1f}  dist={np.linalg.norm(brd4_c_all[idx]):.2f} Å")

# ── BCL6 Lys protrusion analysis ──────────────────────────────────────────────
print("\n=== BCL6 Lys Nζ protrusion above BCL6 surface ===")
lys_resids = set(lys['resnum'] for lys in lys_details)

for lys in lys_details:
    nz = np.array(lys['nz']); ca = np.array(lys['ca'])
    lys_rn = lys['resnum']
    lys_ax = (nz-ca)/np.linalg.norm(nz-ca)

    # All non-Lys BCL6 atoms
    other_atoms = np.array([
        a.coord for res in bcl6_chain if res.id[0]==' ' and res.id[1]!=lys_rn
        for a in res.get_atoms() if a.element not in ('H','')
    ])
    dists = np.linalg.norm(other_atoms - nz, axis=1)
    nearest_idx = np.argmin(dists)
    nearest_d = float(dists[nearest_idx])

    # B-factors of Cα and Nζ
    bf_ca = bcl6_chain[lys_rn]["CA"].bfactor if "CA" in bcl6_chain[lys_rn] else float('nan')
    bf_nz = bcl6_chain[lys_rn]["NZ"].bfactor if "NZ" in bcl6_chain[lys_rn] else float('nan')

    # How far does Nz stick out in the lys_ax direction beyond the nearest BCL6 backbone?
    # = projection of (Nz - nearest_atom) along lys_ax
    nearest_atom_coord = other_atoms[nearest_idx]
    protrusion_along_axis = float(np.dot(nz - nearest_atom_coord, lys_ax))
    lateral_offset       = float(np.sqrt(max(0, nearest_d**2 - protrusion_along_axis**2)))

    print(f"\n  Lys {lys_rn}  SASA={lys['sasa']:.0f} Å²  Bfac(Cα/Nz)={bf_ca:.1f}/{bf_nz:.1f}")
    print(f"    Nz→nearest non-Lys BCL6 atom:   {nearest_d:.2f} Å")
    print(f"    Protrusion along Lys axis:        {protrusion_along_axis:.2f} Å  lateral={lateral_offset:.2f} Å")
    print(f"    Required gap (BRD4 body→Kac-Nz): {d_brd4_entrance:.2f} Å  (BRD4 entrance-side atom)")
    deficit = d_brd4_entrance - protrusion_along_axis
    print(f"    Clash deficit (need protrusion +{deficit:.2f} Å to avoid BRD4 entrance atoms)")

# ── BRD4 pocket entrance atoms explicitly ─────────────────────────────────────
print("\n=== BRD4 pocket entrance residues (closest to Kac-Nz anchor, entrance side) ===")
ent_indices = np.where(ent_mask)[0]
ent_dists   = np.linalg.norm(brd4_c_all[ent_mask], axis=1)
top5 = ent_indices[np.argsort(ent_dists)[:5]]
for idx in top5:
    res_i, atom_i = brd4_res_atoms[idx]
    d = np.linalg.norm(brd4_c_all[idx])
    print(f"  {res_i.resname}{res_i.id[1]:>4} {atom_i.name:>4}  Bfac={atom_i.bfactor:.1f}  "
          f"dist={d:.2f} Å  proj={brd4_proj_all[idx]:.2f}")
