
import numpy as np, pickle

# ── helpers ────────────────────────────────────────────────────────────────────
def rot_v1_to_v2(v1, v2):
    v1 = v1/np.linalg.norm(v1); v2 = v2/np.linalg.norm(v2)
    cr = np.cross(v1, v2); dt = np.clip(np.dot(v1, v2),-1,1)
    cn = np.linalg.norm(cr)
    if cn < 1e-9:
        if dt > 0: return np.eye(3)
        ax = np.cross(v1, [1,0,0] if abs(v1[0])<0.9 else [0,1,0])
        ax /= np.linalg.norm(ax)
        return 2*np.outer(ax,ax)-np.eye(3)
    ax  = cr/cn; ang = np.arctan2(cn, dt)
    K   = np.array([[0,-ax[2],ax[1]],[ax[2],0,-ax[0]],[-ax[1],ax[0],0]])
    return np.eye(3)+np.sin(ang)*K+(1-np.cos(ang))*(K@K)

def rodrigues(ax, angle):
    K = np.array([[0,-ax[2],ax[1]],[ax[2],0,-ax[0]],[-ax[1],ax[0],0]])
    return np.eye(3)+np.sin(angle)*K+(1-np.cos(angle))*(K@K)

# ── Load saved geometry ────────────────────────────────────────────────────────
with open("geom.pkl","rb") as f:
    g = pickle.load(f)
u52_com = g["u52_com"]; eam_com = g["eam_com"]
asn140  = g["asn140"];  pocket_axis = g["pocket_axis"]
surface_lys = g["surface_lys"]

lys_details = g.get("lys_details")
if lys_details is None:
    lys_details = []
    for entry in surface_lys:
        rn = entry['resnum']
        res = bcl6_chain[rn]
        if "CA" in res and "NZ" in res:
            lys_details.append({**entry,
                "ca": res["CA"].coord.copy(), "nz": res["NZ"].coord.copy()})

# ── Correct Kac-Nζ anchor: 4.5 Å from Asn140 along pocket axis ───────────────
# Measured: |Asn140→EAM CoM| = 6.0 Å; Kac Nζ sits ~4.5 Å from Asn140
# (Nζ–C(acetyl) ~1.5 Å, C(acetyl)–Asn140_ND2 H-bond ~3.0 Å)
frac = 4.5 / 6.0
kac_nz_brd4 = asn140 + frac * (eam_com - asn140)
print(f"Kac-Nζ anchor in BRD4 frame: {kac_nz_brd4.round(2)}")
print(f"  |Kac-Nz – Asn140|  = {np.linalg.norm(kac_nz_brd4-asn140):.2f} Å  (target ~4.5 Å)")
print(f"  |Kac-Nz – EAM CoM| = {np.linalg.norm(kac_nz_brd4-eam_com):.2f} Å")

# BRD4 atoms centred on Kac-Nz anchor
brd4_c = brd4_atoms - kac_nz_brd4
asn_c  = asn140 - kac_nz_brd4

# ── BCL6 BTB Lys CA/NZ quick report ──────────────────────────────────────────
print("\nBCL6 surface Lys sidechain lengths (CA→NZ):")
for lys in lys_details:
    ca=np.array(lys['ca']); nz=np.array(lys['nz'])
    print(f"  Lys{lys['resnum']}: |CA–NZ| = {np.linalg.norm(nz-ca):.2f} Å")

# ── Ternary complex: Kac-Nz anchor placed at BCL6 Lys NZ ──────────────────────
# For each Lys: rotate BRD4 pocket_axis → -lys_ax (insertion geometry),
# then sample 36 spin angles around lys_ax; keep the spin with maximum
# (least) min BRD4–BCL6 clash distance.

print("\n" + "="*72)
print("Ternary complex: Kac-Nz anchor @ BCL6-Lys-Nz, spin-optimised")
print(f"{'Lys':>6} {'SASA':>6} {'linker':>7} {'Nz-Asn140':>10} {'best_clash':>11} {'spin°':>6} {'verdict':>10}")
print("-"*72)

ternary_rows = []
for lys in lys_details:
    nz = np.array(lys['nz']); ca = np.array(lys['ca'])
    lys_ax = (nz-ca)/np.linalg.norm(nz-ca)

    # Base rotation: pocket faces BCL6 (pocket_axis → -lys_ax)
    R_base = rot_v1_to_v2(pocket_axis, -lys_ax)

    best_mc = -1.0; best_theta = 0
    for theta in np.linspace(0, 2*np.pi, 36, endpoint=False):
        R_spin = rodrigues(lys_ax, theta)
        R_full = R_spin @ R_base
        b_final = (R_full @ brd4_c.T).T + nz
        # sub-sample BRD4 for speed
        step = max(1, len(b_final)//300)
        d = np.linalg.norm(bcl6_atoms[:,None] - b_final[::step][None,:], axis=2)
        mc = float(d.min())
        if mc > best_mc:
            best_mc = mc; best_theta = theta

    # Asn140 distance in best spin
    R_spin_best = rodrigues(lys_ax, best_theta)
    R_full_best = R_spin_best @ R_base
    asn_final   = R_full_best @ asn_c + nz
    d_asn       = float(np.linalg.norm(nz - asn_final))

    linker_len = float(np.linalg.norm(nz - u52_com))
    verdict = "CLEAR" if best_mc>=3.5 else ("TIGHT" if best_mc>=2.5 else "CLASH")

    ternary_rows.append(dict(resnum=lys['resnum'], sasa=lys['sasa'],
        linker=linker_len, d_asn=d_asn, best_clash=best_mc,
        best_theta=np.degrees(best_theta), verdict=verdict))
    print(f"  K{lys['resnum']:>3}  {lys['sasa']:>5.0f}  {linker_len:>6.1f} Å"
          f"  {d_asn:>8.2f} Å  {best_mc:>9.2f} Å  {np.degrees(best_theta):>5.0f}°  {verdict}")

# Save
with open("geom.pkl","wb") as f:
    pickle.dump({**g, "lys_details":lys_details, "kac_nz_brd4":kac_nz_brd4,
                 "ternary_rows":ternary_rows}, f)
