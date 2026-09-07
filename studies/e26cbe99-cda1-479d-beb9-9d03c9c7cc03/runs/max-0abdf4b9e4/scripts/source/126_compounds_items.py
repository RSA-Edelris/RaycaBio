
from MDAnalysis.analysis import align, rms
import MDAnalysis as mda
import numpy as np

BASE = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"

compounds = {
    "EDS01806218_ent1": (
        f"{BASE}/md_EDS01806218_ent1/complex.gro",
        f"{BASE}/npt_prod_EDS01806218_ent1.xtc",
    ),
    "EDS01806218_ent2": (
        f"{BASE}/md_EDS01806218_ent2/complex.gro",
        f"{BASE}/npt_prod.xtc",
    ),
    "EDS01889984": (
        f"{BASE}/md_EDS01889984/complex.gro",
        f"{BASE}/npt_prod.6304913.xtc",
    ),
}

boresch = {}  # will hold final selections

for name, (gro, xtc) in compounds.items():
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")

    u = mda.Universe(gro, xtc)
    ref = mda.Universe(gro)  # reference = initial structure
    n_frames = len(u.trajectory)

    receptor_ca = u.select_atoms("protein and name CA")
    lig_heavy   = u.select_atoms("resname LIG and not name H*")

    # --- Align on backbone CA (frames 500..1000, last ~5 ns) ---
    aligner = align.AlignTraj(u, ref, select="protein and name CA",
                              in_memory=True).run(start=500)

    # --- RMSF on aligned trajectory ---
    from MDAnalysis.analysis.rms import RMSF as MDA_RMSF
    rmsf_ca_obj  = MDA_RMSF(receptor_ca).run(start=500)
    rmsf_lig_obj = MDA_RMSF(lig_heavy).run(start=500)
    ca_rmsf  = rmsf_ca_obj.results.rmsf
    lig_rmsf = rmsf_lig_obj.results.rmsf

    # Last frame for geometry
    u.trajectory[-1]
    lig_center = lig_heavy.positions.mean(axis=0)

    # ---- Receptor candidates (CA within 12 Å of ligand, lowest RMSF) ----
    dist_ca = np.linalg.norm(receptor_ca.positions - lig_center, axis=1)
    nearby  = np.where(dist_ca < 12.0)[0]
    sorted_ca = nearby[np.argsort(ca_rmsf[nearby])]

    print(f"  CA within 12 Å: {len(nearby)}")
    print("  Top-10 lowest-RMSF receptor CAs (aligned):")
    r_cands = []
    for ni in sorted_ca[:10]:
        at = receptor_ca[ni]
        print(f"    idx={at.index+1:5d} resid={at.resid:4d} {at.resname}  "
              f"RMSF={ca_rmsf[ni]:.3f}Å  dist_lig={dist_ca[ni]:.1f}Å")
        r_cands.append((at.index+1, at.resid, at.resname, ca_rmsf[ni], dist_ca[ni], at.position.copy()))

    # ---- Ligand candidates (lowest RMSF) ----
    lig_sorted = np.argsort(lig_rmsf)
    print("  Top-5 lowest-RMSF ligand heavy atoms (aligned):")
    l_cands = []
    for i in lig_sorted[:5]:
        at = lig_heavy[i]
        print(f"    idx={at.index+1:5d} {at.name:5s} {at.type:4s}  RMSF={lig_rmsf[i]:.3f}Å")
        l_cands.append((at.index+1, at.name, at.type, lig_rmsf[i], at.position.copy()))

    # ---- Select Boresch atoms with geometry checks ----
    # l1 = lowest-RMSF ligand heavy atom
    l1_idx, l1_name, l1_type, l1_rmsf, l1_pos = l_cands[0]
    # r1 = lowest-RMSF receptor CA closest to l1
    best_r1 = None
    for r_idx, r_resid, r_resname, r_rmsf, r_dist, r_pos in r_cands:
        d = np.linalg.norm(r_pos - l1_pos)
        if 3.0 < d < 10.0:
            best_r1 = (r_idx, r_resid, r_resname, r_rmsf, r_pos)
            break
    if best_r1 is None:
        best_r1 = (r_cands[0][0], r_cands[0][1], r_cands[0][2], r_cands[0][3], r_cands[0][5])

    r1_idx, r1_resid, r1_resname, _, r1_pos = best_r1
    r1_l1_dist = np.linalg.norm(r1_pos - l1_pos)

    # l2, l3 = next lowest-RMSF lig atoms, angle r1-l1-l2 must be in (30°,150°)
    l2_data = None
    l3_data = None
    for i in lig_sorted[1:]:
        at = lig_heavy[i]
        pos = at.position.copy()
        v1 = r1_pos - l1_pos; v2 = pos - l1_pos
        cos_a = np.dot(v1, v2) / (np.linalg.norm(v1)*np.linalg.norm(v2) + 1e-9)
        angle = np.degrees(np.arccos(np.clip(cos_a, -1, 1)))
        if 20 < angle < 160:
            if l2_data is None:
                l2_data = (at.index+1, at.name, lig_rmsf[i], pos, angle)
            else:
                # check l2-l3 angle at l2
                v3 = l2_data[3] - l1_pos; v4 = pos - l2_data[3]
                cos_b = np.dot(v3, v4) / (np.linalg.norm(v3)*np.linalg.norm(v4) + 1e-9)
                ang2 = np.degrees(np.arccos(np.clip(cos_b, -1, 1)))
                if 20 < ang2 < 160:
                    l3_data = (at.index+1, at.name, lig_rmsf[i], pos)
                    break

    # r2, r3 from remaining receptor candidates, checking r2-r1-l1 angle
    r2_data = None; r3_data = None
    for r_idx, r_resid, r_resname, r_rmsf, r_dist, r_pos in r_cands:
        if r_idx == r1_idx:
            continue
        v1 = r_pos - r1_pos; v2 = l1_pos - r1_pos
        cos_a = np.dot(v1, v2) / (np.linalg.norm(v1)*np.linalg.norm(v2) + 1e-9)
        angle = np.degrees(np.arccos(np.clip(cos_a, -1, 1)))
        if 20 < angle < 160:
            if r2_data is None:
                r2_data = (r_idx, r_resid, r_resname, r_rmsf, r_pos, angle)
            elif r3_data is None:
                r3_data = (r_idx, r_resid, r_resname, r_rmsf, r_pos)
                break

    # ---- Compute equilibrium Boresch values ----
    def dih(a,b,c,d):
        """IUPAC dihedral in degrees"""
        b1 = b-a; b2 = c-b; b3 = d-c
        n1 = np.cross(b1,b2); n2 = np.cross(b2,b3)
        n1n = n1/(np.linalg.norm(n1)+1e-9); n2n = n2/(np.linalg.norm(n2)+1e-9)
        x = np.dot(n1n,n2n); y = np.dot(np.cross(n1n,b2/np.linalg.norm(b2+1e-9)),n2n)
        return np.degrees(np.arctan2(y,x))

    def ang(a,b,c):
        v1=a-b; v2=c-b
        return np.degrees(np.arccos(np.clip(np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)+1e-9),-1,1)))

    r3p = r3_data[4] if r3_data else r2_data[4]+np.array([3,0,0])
    l2p = l2_data[3] if l2_data else l1_pos + np.array([0,1.5,0])
    l3p = l3_data[3] if l3_data else l1_pos + np.array([1,1,0])

    r0   = r1_l1_dist / 10.0  # Å → nm
    tA   = ang(r2_data[4], r1_pos, l1_pos)
    tB   = ang(r1_pos, l1_pos, l2p)
    pA   = dih(r3p, r2_data[4], r1_pos, l1_pos)
    pB   = dih(r2_data[4], r1_pos, l1_pos, l2p)
    pC   = dih(r1_pos, l1_pos, l2p, l3p)

    print(f"\n  >> Boresch selection:")
    print(f"     r1={r1_idx} ({r1_resname}{r1_resid})")
    print(f"     r2={r2_data[0]} ({r2_data[2]}{r2_data[1]})")
    print(f"     r3={r3_data[0] if r3_data else 'N/A'}")
    print(f"     l1={l1_idx} ({l1_name})")
    print(f"     l2={l2_data[0] if l2_data else 'N/A'} ({l2_data[1] if l2_data else 'N/A'})")
    print(f"     l3={l3_data[0] if l3_data else 'N/A'} ({l3_data[1] if l3_data else 'N/A'})")
    print(f"  >> Equilibrium: r0={r0:.4f} nm  tA={tA:.1f}°  tB={tB:.1f}°  pA={pA:.1f}°  pB={pB:.1f}°  pC={pC:.1f}°")

    # ---- Analytical Boresch restraint release correction ----
    # ΔG_restr_release = +kT * ln( 8π²V₀ / (r₀² sinθA sinθB (2πkT)^3 / (kr kθA kθB kφA kφB kφC)^(1/2) ))
    kT   = 2.479  # kJ/mol at 300 K (= 8.314e-3 × 300)
    V0   = 1.661  # nm³ (1 L/mol standard state concentration = 1 M)
    k_r  = 4184.0  # kJ/mol/nm²  (= 10 kcal/mol/Å²)
    k_a  = 41.84   # kJ/mol/rad² (= 10 kcal/mol/rad²)
    sinA = np.sin(np.radians(tA))
    sinB = np.sin(np.radians(tB))
    # Gaussian integrals for distance (harmonic): sqrt(2π kT / k_r) × r0²
    # Full Boresch formula:
    sigma_r  = np.sqrt(2 * np.pi * kT / k_r)
    sigma_a  = np.sqrt(2 * np.pi * kT / k_a)  # each angular coordinate
    Z_conf   = (r0**2 * sinA * sinB * sigma_r * sigma_a**5) / (2 * np.pi)
    dG_restr = kT * np.log(8 * np.pi**2 * V0 / Z_conf)  # kJ/mol
    dG_restr_kcal = dG_restr / 4.184
    print(f"  >> Analytical restraint release: ΔG_restr = {dG_restr:.2f} kJ/mol  ({dG_restr_kcal:.2f} kcal/mol)")

    boresch[name] = dict(
        r1=r1_idx, r2=r2_data[0], r3=(r3_data[0] if r3_data else r2_data[0]),
        l1=l1_idx, l2=(l2_data[0] if l2_data else l1_idx+1),
        l3=(l3_data[0] if l3_data else l1_idx+2),
        r0=r0, tA=tA, tB=tB, pA=pA, pB=pB, pC=pC,
        dG_restr_kJ=dG_restr, dG_restr_kcal=dG_restr_kcal,
        u=u,
    )

print("\n\n=== Summary ===")
for name, d in boresch.items():
    print(f"{name}: r1={d['r1']} r2={d['r2']} r3={d['r3']}  "
          f"l1={d['l1']} l2={d['l2']} l3={d['l3']}  "
          f"r0={d['r0']:.3f}nm  ΔG_restr={d['dG_restr_kcal']:.2f} kcal/mol")
