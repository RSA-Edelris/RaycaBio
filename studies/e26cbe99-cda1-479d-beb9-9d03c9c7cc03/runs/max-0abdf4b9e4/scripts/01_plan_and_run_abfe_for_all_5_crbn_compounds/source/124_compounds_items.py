
import MDAnalysis as mda
from MDAnalysis.analysis.rms import RMSF
import numpy as np
import os

BASE = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"

# Map compound name -> (structure_gro, trajectory_xtc)
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

results = {}

for name, (gro, xtc) in compounds.items():
    print(f"\n=== {name} ===")
    u = mda.Universe(gro, xtc)
    print(f"  Atoms: {len(u.atoms)}, Frames: {len(u.trajectory)}")
    
    # Identify receptor CA and ligand heavy atoms
    receptor_ca = u.select_atoms("protein and name CA")
    ligand_heavy = u.select_atoms("resname LIG and not name H*")
    print(f"  Receptor CAs: {len(receptor_ca)}, Ligand heavy: {len(len(ligand_heavy) and [len(ligand_heavy)] or [0])[0]}")
    
    # RMSF over last 500 frames (frames 500-1000, last ~5 ns)
    start_frame = 500
    
    rmsf_ca = RMSF(receptor_ca).run(start=start_frame)
    rmsf_lig = RMSF(ligand_heavy).run(start=start_frame)
    
    ca_rmsf = rmsf_ca.results.rmsf
    lig_rmsf_vals = rmsf_lig.results.rmsf
    
    # Get last frame for geometry
    u.trajectory[-1]
    lig_center = ligand_heavy.positions.mean(axis=0)
    
    # Receptor CA candidates: within 15 Å of ligand centroid, sorted by RMSF
    dist_to_lig = np.linalg.norm(receptor_ca.positions - lig_center, axis=1)
    nearby_mask = dist_to_lig < 15.0
    nearby_idx = np.where(nearby_mask)[0]
    nearby_rmsf = ca_rmsf[nearby_idx]
    sorted_nearby = nearby_idx[np.argsort(nearby_rmsf)]
    
    print(f"  CAs within 15A of ligand: {len(nearby_idx)}")
    print(f"  Top-10 lowest RMSF CAs (GROMACS 1-based index, residue, RMSF):")
    top_ca_idx = []
    for i, ni in enumerate(sorted_nearby[:10]):
        at = receptor_ca[ni]
        print(f"    [{i}] gromacs_idx={at.index+1} resid={at.resid} resname={at.resname} RMSF={ca_rmsf[ni]:.3f} Å dist={dist_to_lig[ni]:.1f} Å")
        top_ca_idx.append(ni)
    
    # Ligand atoms: sorted by RMSF
    lig_sorted = np.argsort(lig_rmsf_vals)
    print(f"  Top-5 lowest RMSF ligand heavy atoms (GROMACS 1-based index, name, RMSF):")
    top_lig_idx = []
    for i in lig_sorted[:5]:
        at = ligand_heavy[i]
        print(f"    [{i}] gromacs_idx={at.index+1} name={at.name} type={at.type} RMSF={lig_rmsf_vals[i]:.3f} Å")
        top_lig_idx.append(i)
    
    results[name] = {
        "receptor_ca": receptor_ca,
        "ligand_heavy": ligand_heavy,
        "ca_rmsf": ca_rmsf,
        "lig_rmsf": lig_rmsf_vals,
        "sorted_ca_nearby": sorted_nearby,
        "sorted_lig": lig_sorted,
        "lig_center": lig_center,
    }

print("\nDone — RMSF analysis complete.")
