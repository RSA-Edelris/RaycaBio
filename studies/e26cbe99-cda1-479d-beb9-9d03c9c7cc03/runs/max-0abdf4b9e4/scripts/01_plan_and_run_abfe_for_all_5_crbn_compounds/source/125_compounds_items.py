
import MDAnalysis as mda
from MDAnalysis.analysis.rms import RMSF
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

boresch_atoms = {}

for name, (gro, xtc) in compounds.items():
    print(f"\n=== {name} ===")
    u = mda.Universe(gro, xtc)
    n_frames = len(u.trajectory)
    print(f"  Atoms: {len(u.atoms)}, Frames: {n_frames}")

    receptor_ca = u.select_atoms("protein and name CA")
    ligand_heavy = u.select_atoms("resname LIG and not name H*")
    print(f"  Receptor CAs: {len(receptor_ca)},  Ligand heavy: {len(ligand_heavy)}")

    start_frame = 500  # last ~5 ns

    rmsf_ca_obj  = RMSF(receptor_ca).run(start=start_frame)
    rmsf_lig_obj = RMSF(ligand_heavy).run(start=start_frame)
    ca_rmsf  = rmsf_ca_obj.results.rmsf
    lig_rmsf = rmsf_lig_obj.results.rmsf

    # Use last frame for geometry
    u.trajectory[-1]
    lig_center = ligand_heavy.positions.mean(axis=0)

    # Receptor candidates: CA within 15 Å of ligand centroid, sorted by RMSF
    dist_ca = np.linalg.norm(receptor_ca.positions - lig_center, axis=1)
    nearby  = np.where(dist_ca < 15.0)[0]
    sorted_ca = nearby[np.argsort(ca_rmsf[nearby])]

    print(f"  CA atoms within 15 Å of ligand: {len(nearby)}")
    print("  Top-10 lowest-RMSF receptor CAs:")
    top_r_list = []
    for ni in sorted_ca[:10]:
        at = receptor_ca[ni]
        print(f"    GROMACS_idx={at.index+1:5d}  resid={at.resid:4d}  resname={at.resname}  "
              f"RMSF={ca_rmsf[ni]:.3f}Å  dist={dist_ca[ni]:.1f}Å")
        top_r_list.append(at.index + 1)  # 1-based GROMACS

    # Ligand atoms sorted by RMSF
    lig_sorted_idx = np.argsort(lig_rmsf)
    print("  Top-5 lowest-RMSF ligand heavy atoms:")
    top_l_list = []
    for i in lig_sorted_idx[:5]:
        at = ligand_heavy[i]
        print(f"    GROMACS_idx={at.index+1:5d}  name={at.name:4s}  type={at.type:4s}  "
              f"RMSF={lig_rmsf[i]:.3f}Å")
        top_l_list.append(at.index + 1)

    boresch_atoms[name] = {
        "top_r_gmx": top_r_list,  # 1-based
        "top_l_gmx": top_l_list,
        "receptor_ca": receptor_ca,
        "ligand_heavy": ligand_heavy,
        "ca_rmsf": ca_rmsf,
        "lig_rmsf": lig_rmsf,
        "sorted_ca": sorted_ca,
        "lig_sorted_idx": lig_sorted_idx,
        "universe": u,
    }

print("\n=== Done ===")
