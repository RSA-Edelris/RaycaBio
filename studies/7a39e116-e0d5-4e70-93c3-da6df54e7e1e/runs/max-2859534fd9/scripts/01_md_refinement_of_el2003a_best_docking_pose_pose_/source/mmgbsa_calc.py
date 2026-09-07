#!/usr/bin/env python3
"""
1-trajectory MM-GBSA from GROMACS MD output.
GROMACS topology  →  ParmEd  →  AMBER prmtop  →  OpenMM OBC2 per-frame energies.
ΔG_bind = mean(E_complex - E_receptor - E_ligand)  over 100 frames (1 ns).
"""
import os, json, sys
import numpy as np

WORK = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/gbsa_run/EL2003A_pose2"
OUT  = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/mmgbsa_result.json"
TMP  = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/mmgbsa_tmp"
os.makedirs(TMP, exist_ok=True)

print("=== MM-GBSA calculation ===")
print(f"Work dir : {WORK}")

import parmed as pmd
print(f"ParmEd   : {pmd.__version__}")

import mdtraj as mdt
print(f"MDTraj   : {mdt.__version__}")

import openmm as mm
import openmm.app as app
import openmm.unit as unit
print(f"OpenMM   : {mm.__version__}")

# ── 1. Load GROMACS topology ────────────────────────────────────────────────
print("\n[1] Loading GROMACS topology + structure...")
top_file = os.path.join(WORK, "complex.top")
pdb_file = os.path.join(WORK, "complex_reres.pdb")
gmx = pmd.load_file(top_file, xyz=pdb_file)
print(f"    Atoms: {len(gmx.atoms)}, Residues: {len(gmx.residues)}")

# ── 2. Identify ligand / receptor atom sets ─────────────────────────────────
lig_idx = [a.idx for a in gmx.atoms if a.residue.name == "MOL"]
rec_idx = [a.idx for a in gmx.atoms if a.residue.name != "MOL"]
print(f"[2] Receptor atoms: {len(rec_idx)}, Ligand atoms: {len(lig_idx)}")
if not lig_idx:
    raise RuntimeError("No 'MOL' residue found in topology")

# ── 3. Apply OBC2-compatible GB radii (mbondi2) ─────────────────────────────
print("[3] Assigning mbondi2 GB radii...")
try:
    from parmed.tools import changeRadii
    changeRadii(gmx, 'mbondi2').execute()
    print("    changeRadii OK")
except Exception as e:
    print(f"    changeRadii failed ({e}); assigning radii manually...")
    # Fallback: element-based mbondi2 radii
    _radii = {'H': 1.2, 'C': 1.7, 'N': 1.55, 'O': 1.5, 'S': 1.8, 'P': 1.85, 'F': 1.5,
              'Cl': 1.7, 'Br': 1.85, 'I': 1.98}
    _screen = {'H': 0.85, 'C': 0.72, 'N': 0.79, 'O': 0.85, 'S': 0.96, 'P': 0.86, 'F': 0.88,
               'Cl': 0.75, 'Br': 0.88, 'I': 0.99}
    for a in gmx.atoms:
        elem = a.element_name.capitalize() if a.element_name else 'C'
        a.solvent_radius = _radii.get(elem, 1.5)
        a.screen          = _screen.get(elem, 0.80)

# ── 4. Write AMBER prmtop files for complex / receptor / ligand ─────────────
print("[4] Writing AMBER prmtop files...")

cplx_top = os.path.join(TMP, "complex.prmtop")
rec_top  = os.path.join(TMP, "receptor.prmtop")
lig_top  = os.path.join(TMP, "ligand.prmtop")

gmx.save(cplx_top, overwrite=True)
gmx[rec_idx].save(rec_top, overwrite=True)
gmx[lig_idx].save(lig_top, overwrite=True)
print(f"    Wrote: complex.prmtop, receptor.prmtop, ligand.prmtop")

# ── 5. Build OpenMM OBC2 contexts ───────────────────────────────────────────
def obc2_context(prmtop_path):
    top = app.AmberPrmtopFile(prmtop_path)
    sys = top.createSystem(
        implicitSolvent=app.OBC2,
        nonbondedMethod=app.NoCutoff,
        constraints=None,
        removeCMMotion=False,
        soluteDielectric=1.0,
        solventDielectric=80.0,
    )
    integrator = mm.VerletIntegrator(0.001)
    platform = mm.Platform.getPlatformByName("CPU")
    ctx = mm.Context(sys, integrator, platform)
    return ctx

print("[5] Building OpenMM OBC2 contexts...")
ctx_c = obc2_context(cplx_top)
ctx_r = obc2_context(rec_top)
ctx_l = obc2_context(lig_top)
print("    Contexts ready.")

# ── 6. Load trajectory ───────────────────────────────────────────────────────
print("[6] Loading trajectory...")
traj_path = os.path.join(WORK, "traj_com.xtc")
traj = mdt.load(traj_path, top=pdb_file)
print(f"    Frames: {traj.n_frames}, Atoms: {traj.n_atoms}")

# ── 7. Per-frame MM-GBSA energies ────────────────────────────────────────────
print("[7] Computing per-frame energies (OBC2)...")
kcal = unit.kilocalories_per_mole
records = []
for i in range(traj.n_frames):
    xyz_nm = traj.xyz[i]                  # (n_atoms, 3) in nm

    ctx_c.setPositions(xyz_nm[             :] * unit.nanometer)
    ctx_r.setPositions(xyz_nm[rec_idx      ] * unit.nanometer)
    ctx_l.setPositions(xyz_nm[lig_idx      ] * unit.nanometer)

    Ec = ctx_c.getState(getEnergy=True).getPotentialEnergy().value_in_unit(kcal)
    Er = ctx_r.getState(getEnergy=True).getPotentialEnergy().value_in_unit(kcal)
    El = ctx_l.getState(getEnergy=True).getPotentialEnergy().value_in_unit(kcal)
    dG = Ec - Er - El

    records.append({"frame": i, "time_ps": float(traj.time[i]),
                    "E_complex": Ec, "E_receptor": Er, "E_ligand": El, "dG_bind": dG})
    if i % 10 == 0:
        print(f"    frame {i:3d}  t={traj.time[i]:.0f} ps  dG={dG:.2f} kcal/mol")

# ── 8. Statistics ────────────────────────────────────────────────────────────
dGs = [r["dG_bind"] for r in records]
# Discard first 10 frames (100 ps equilibration)
dGs_prod = dGs[10:]
mean_dG = float(np.mean(dGs_prod))
std_dG  = float(np.std(dGs_prod))
sem_dG  = float(np.std(dGs_prod) / np.sqrt(len(dGs_prod)))

print(f"\n=== MM-GBSA Result ===")
print(f"  Frames analysed    : {len(dGs_prod)} (frames 10–99, 100–1000 ps)")
print(f"  ΔG_bind (mean)     : {mean_dG:.3f} kcal/mol")
print(f"  ΔG_bind (SD)       : {std_dG:.3f} kcal/mol")
print(f"  ΔG_bind (SEM)      : {sem_dG:.3f} kcal/mol")
print(f"  Prior EM-mode value: -61.835 kcal/mol")

result = {
    "compound": "EL2003A",
    "pose": "pose2",
    "method": "MM-GBSA OBC2 (1-trajectory, GROMACS AMBER03+GAFF2, 1 ns)",
    "n_frames_total": len(dGs),
    "n_frames_prod": len(dGs_prod),
    "dG_bind_mean_kcal_mol": mean_dG,
    "dG_bind_std_kcal_mol":  std_dG,
    "dG_bind_sem_kcal_mol":  sem_dG,
    "em_mode_reference_kcal_mol": -61.835,
    "per_frame": records,
}

with open(OUT, "w") as f:
    json.dump(result, f, indent=2)
print(f"\nSaved: {OUT}")
