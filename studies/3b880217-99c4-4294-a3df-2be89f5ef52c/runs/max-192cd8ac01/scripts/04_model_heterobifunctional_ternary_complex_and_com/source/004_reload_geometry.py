
import numpy as np, pickle

# ── reload geometry ────────────────────────────────────────────────────────────
with open("geom.pkl","rb") as f:
    g = pickle.load(f)

u52_com      = g["u52_com"]
eam_com      = g["eam_com"]
asn140       = g["asn140"]
pocket_axis  = g["pocket_axis"]          # Asn140→entrance (unit)
surface_lys  = g["surface_lys"]
surface_serthr = g["surface_serthr"]

# ── get BCL6 Lys Cα coords from structure ────────────────────────────────────
lys_details = []
for entry in surface_lys:
    rn = entry['resnum']
    res = bcl6_chain[rn]
    if "CA" in res and "NZ" in res:
        lys_details.append({
            **entry,
            "ca": res["CA"].coord.copy(),
            "nz": res["NZ"].coord.copy(),
        })

# ── get all BRD4/BCL6 heavy-atom arrays ───────────────────────────────────────
brd4_atoms = np.array([
    a.coord for res in brd4[0]["A"] if res.id[0]==' '
    for a in res.get_atoms() if a.element not in ('H','')
])
bcl6_atoms = np.array([
    a.coord for res in bcl6_chain if res.id[0]==' '
    for a in res.get_atoms() if a.element not in ('H','')
])
# BRD4 atoms centred on EAM CoM (for rotation)
brd4_centred = brd4_atoms - eam_com
asn140_c     = asn140      - eam_com   # centred Asn140

def rot_v1_to_v2(v1, v2):
    """Rotation matrix that rotates unit vector v1 onto unit vector v2."""
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    cr = np.cross(v1, v2)
    dt = np.clip(np.dot(v1, v2), -1, 1)
    cn = np.linalg.norm(cr)
    if cn < 1e-9:
        if dt > 0:
            return np.eye(3)
        ax = np.cross(v1, [1,0,0] if abs(v1[0])<0.9 else [0,1,0])
        ax /= np.linalg.norm(ax)
        return 2*np.outer(ax,ax) - np.eye(3)
    ax  = cr / cn
    ang = np.arctan2(cn, dt)
    K   = np.array([[0,-ax[2],ax[1]],[ax[2],0,-ax[0]],[-ax[1],ax[0],0]])
    return np.eye(3) + np.sin(ang)*K + (1-np.cos(ang))*(K@K)

# ── ternary complex analysis for each surface Lys ────────────────────────────
print("Ternary complex geometry: BRD4 pocket entrance placed at BCL6 Lys Nζ")
print("Rotation: pocket axis aligned anti-parallel to BCL6 Lys Cα→Nζ axis")
print("="*72)

results = []
for lys in lys_details:
    ca  = np.array(lys["ca"]); nz = np.array(lys["nz"])
    lys_ax = (nz - ca) / np.linalg.norm(nz - ca)          # Cα→Nζ unit vector

    # Rotate BRD4 so pocket_axis maps onto -lys_ax (pocket faces BCL6 Lys)
    R = rot_v1_to_v2(pocket_axis, -lys_ax)

    # Apply rotation around EAM CoM, then translate to Lys Nζ
    brd4_final  = (R @ brd4_centred.T).T + nz
    asn140_final = R @ asn140_c + nz

    # Steric clash: min inter-protein heavy-atom distance
    # Use a sub-sample of BCL6 atoms (all, BRD4 subset) for speed
    step = max(1, len(brd4_final)//500)
    d_mat   = np.linalg.norm(
        bcl6_atoms[:, np.newaxis] - brd4_final[::step][np.newaxis, :], axis=2
    )
    min_clash = float(d_mat.min())

    # Distance from Lys Nζ to (rotated) Asn140 ND2
    d_nz_asn = float(np.linalg.norm(nz - asn140_final))

    # Approach angle verification (should be ~0 by construction, sanity check)
    asn_to_nz_dir = (nz - asn140_final) / np.linalg.norm(nz - asn140_final)
    approach_angle = float(np.degrees(np.arccos(np.clip(np.dot(asn_to_nz_dir, lys_ax), -1,1))))

    # Required linker length = dist from U52 CoM (BCL6 anchor) to Lys Nζ
    linker_len = float(np.linalg.norm(nz - u52_com))

    results.append(dict(
        resnum=lys["resnum"], sasa=lys["sasa"],
        nz=nz, linker_len=linker_len,
        d_nz_asn=d_nz_asn, min_clash=min_clash,
        approach_angle=approach_angle,
    ))
    print(f"\n  Lys {lys['resnum']}  SASA={lys['sasa']:.0f} Å²")
    print(f"    Required linker length (BCL6-anchor → Nζ): {linker_len:.1f} Å")
    print(f"    Nζ → Asn140 ND2 in ternary complex:        {d_nz_asn:.1f} Å")
    print(f"    Approach angle (Lys-axis vs pocket-axis):   {approach_angle:.1f}°  (0=ideal)")
    print(f"    Min BRD4-BCL6 heavy-atom distance:          {min_clash:.1f} Å  (clash<3.5 Å)")
    status = "CLASH" if min_clash < 3.5 else ("OK" if min_clash < 6 else "CLEAR")
    print(f"    Steric verdict: {status}")

# Save for downstream
with open("geom.pkl","wb") as f:
    pickle.dump({**g, "lys_details": lys_details, "ternary_results": results}, f)
