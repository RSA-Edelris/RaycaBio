
import subprocess, os, shutil
import MDAnalysis as mda
import numpy as np

BASE = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"
AMBER = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca"
TLEAP = f"{AMBER}/bin/tleap"

# -- Boresch parameters from RMSF analysis --
BP = {
    "EDS01806218_ent1": dict(
        r1=1268, r2=1289, r3=1200, l1=2282, l2=2266, l3=2267,
        r0=0.8406, tA=100.9, tB=77.0, pA=-63.7, pB=-114.1, pC=-57.9,
        dG_kcal=7.33, traj="npt_prod_EDS01806218_ent1.xtc",
        mol_name="EDS01806218"),
    "EDS01806218_ent2": dict(
        r1=1179, r2=1200, r3=1635, l1=2288, l2=2290, l3=2286,
        r0=0.8128, tA=78.9, tB=90.0, pA=30.3, pB=139.2, pC=-75.1,
        dG_kcal=7.36, traj="npt_prod.xtc",
        mol_name="EDS01806218"),
    "EDS01889984": dict(
        r1=1216, r2=1635, r3=1238, l1=2281, l2=2282, l3=2279,
        r0=0.7066, tA=32.8, tB=101.6, pA=-32.0, pB=-46.7, pC=-103.6,
        dG_kcal=7.89, traj="npt_prod.6304913.xtc",
        mol_name="EDS01889984"),
}

# Lambda schedule (17 windows)
COUL = [0.00, 0.25, 0.50, 0.75, 1.00, 1.00, 1.00, 1.00, 1.00,
        1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00]
VDW  = [0.00, 0.00, 0.00, 0.00, 0.00, 0.10, 0.20, 0.30, 0.40,
        0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.95, 1.00]
N_WIN = len(COUL)
COUL_STR = " ".join(f"{v:.2f}" for v in COUL)
VDW_STR  = " ".join(f"{v:.2f}" for v in VDW)

K_B = 4184.0   # kJ/mol/nm²
K_A = 41.84    # kJ/mol/rad²

# ======================================================================
# Step 1: Extract last frame of each complex trajectory
# ======================================================================
print("=== Step 1: Extract last frames ===")
for name, p in BP.items():
    md_dir = f"{BASE}/md_{name}"
    out_gro = f"{md_dir}/abfe_start.gro"
    if os.path.exists(out_gro):
        print(f"  {name}: abfe_start.gro already exists, skipping")
        continue
    u = mda.Universe(f"{md_dir}/complex.gro", f"{BASE}/{p['traj']}")
    u.trajectory[-1]  # last frame
    with mda.Writer(out_gro) as W:
        W.write(u.atoms)
    sz = os.path.getsize(out_gro)
    print(f"  {name}: wrote abfe_start.gro ({sz//1024} KB, {len(u.atoms)} atoms, last frame)")

# ======================================================================
# Step 2: Create solvent-leg tleap inputs and run tleap
# ======================================================================
print("\n=== Step 2: Solvate ligand for solvent leg ===")
for name, p in BP.items():
    md_dir = f"{BASE}/md_{name}"
    abfe_dir = f"{md_dir}/abfe_solv"
    os.makedirs(abfe_dir, exist_ok=True)

    tleap_in = f"{abfe_dir}/tleap_solv.in"
    prmtop   = f"{abfe_dir}/lig_solv.prmtop"
    inpcrd   = f"{abfe_dir}/lig_solv.inpcrd"

    if os.path.exists(prmtop):
        print(f"  {name}: lig_solv.prmtop already exists, skipping")
        continue

    # Write tleap input — solvate ligand alone with 12 Å TIP3P box
    tleap_content = f"""source leaprc.gaff2
source leaprc.water.tip3p
loadamberparams {md_dir}/ligand.frcmod
LIG = loadmol2 {md_dir}/ligand.mol2
solvateBox LIG TIP3PBOX 12.0
addIons2 LIG Na+ 0.15
addIons2 LIG Cl- 0.15
saveamberparm LIG {prmtop} {inpcrd}
quit
"""
    with open(tleap_in, "w") as f:
        f.write(tleap_content)

    result = subprocess.run(
        [TLEAP, "-f", tleap_in],
        capture_output=True, text=True, cwd=abfe_dir
    )
    if result.returncode != 0 or not os.path.exists(prmtop):
        print(f"  {name}: tleap FAILED")
        print(result.stderr[-500:])
    else:
        sz = os.path.getsize(prmtop)
        print(f"  {name}: lig_solv.prmtop created ({sz//1024} KB)")

print("\nStep 1 & 2 done.")
