
import subprocess, os

# ======================================================================
# Step 3: Convert solvent-leg prmtop → GROMACS via subprocess
#         (avoid parmed/pdb import conflict in sandbox)
# ======================================================================
print("=== Step 3: ParmEd conversion (subprocess) ===")

PYTHON = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/python"

parmed_script = """
import sys, parmed as pmd
name, base = sys.argv[1], sys.argv[2]
sv_dir  = f"{base}/md_{name}/abfe_solv"
prmtop  = f"{sv_dir}/lig_solv.prmtop"
inpcrd  = f"{sv_dir}/lig_solv.inpcrd"
struct = pmd.load_file(prmtop, inpcrd)
struct.save(f"{sv_dir}/lig_solv.top", overwrite=True)
struct.save(f"{sv_dir}/lig_solv.gro", overwrite=True)
print(f"OK {len(struct.atoms)} atoms")
"""

script_path = f"{BASE}/abfe_parmed_conv.py"
with open(script_path, "w") as f:
    f.write(parmed_script)

for name in BP:
    sv_dir  = f"{BASE}/md_{name}/abfe_solv"
    top_out = f"{sv_dir}/lig_solv.top"
    gro_out = f"{sv_dir}/lig_solv.gro"

    if os.path.exists(top_out) and os.path.exists(gro_out):
        import os as _os
        sz = _os.path.getsize(top_out)
        print(f"  {name}: already converted ({sz//1024} KB), skipping")
        continue

    r = subprocess.run([PYTHON, script_path, name, BASE],
                       capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(top_out):
        print(f"  {name}: FAILED\n{r.stderr[-300:]}")
    else:
        print(f"  {name}: {r.stdout.strip()}")

# ======================================================================
# Step 4: Add Boresch restraints to complex.top
# ======================================================================
print("\n=== Step 4: Add Boresch restraints to complex.top ===")

def boresch_section(p):
    r1,r2,r3 = p['r1'], p['r2'], p['r3']
    l1,l2,l3 = p['l1'], p['l2'], p['l3']
    r0 = p['r0']
    tA, tB = p['tA'], p['tB']
    pA, pB, pC = p['pA'], p['pB'], p['pC']
    return (
        "\n[ intermolecular_interactions ]\n"
        "; Boresch 6-DOF restraints — constant in both lambda states\n"
        "[ bonds ]\n"
        f"; ai    aj    funct  b0_A     kb_A        b0_B     kb_B\n"
        f"  {r1:5d} {l1:5d}    1    {r0:.4f}   {K_B:.1f}   {r0:.4f}   {K_B:.1f}\n"
        "[ angles ]\n"
        f"; ai    aj    ak    funct  t0_A    kt_A    t0_B    kt_B\n"
        f"  {r2:5d} {r1:5d} {l1:5d}    1    {tA:.2f}   {K_A:.2f}   {tA:.2f}   {K_A:.2f}\n"
        f"  {r1:5d} {l1:5d} {l2:5d}    1    {tB:.2f}   {K_A:.2f}   {tB:.2f}   {K_A:.2f}\n"
        "[ dihedrals ]\n"
        f"; ai    aj    ak    al    funct  phi0_A   kd_A   phi0_B   kd_B\n"
        f"  {r3:5d} {r2:5d} {r1:5d} {l1:5d}    2    {pA:.2f}   {K_A:.2f}   {pA:.2f}   {K_A:.2f}\n"
        f"  {r2:5d} {r1:5d} {l1:5d} {l2:5d}    2    {pB:.2f}   {K_A:.2f}   {pB:.2f}   {K_A:.2f}\n"
        f"  {r1:5d} {l1:5d} {l2:5d} {l3:5d}    2    {pC:.2f}   {K_A:.2f}   {pC:.2f}   {K_A:.2f}\n"
    )

for name, p in BP.items():
    md_dir  = f"{BASE}/md_{name}"
    top_in  = f"{md_dir}/complex.top"
    top_out = f"{md_dir}/complex_abfe.top"
    if os.path.exists(top_out):
        print(f"  {name}: already exists, skipping")
        continue
    with open(top_in) as f:
        content = f.read()
    content += boresch_section(p)
    with open(top_out, "w") as f:
        f.write(content)
    print(f"  {name}: complex_abfe.top  (r1={p['r1']}, l1={p['l1']}, r0={p['r0']:.3f} nm)")

# ======================================================================
# Step 5: Write FEP MDP files
# ======================================================================
print("\n=== Step 5: Write FEP MDP files ===")

def fep_mdp(window, leg, name):
    tc_grps = "Protein_LIG Water_and_ions" if leg == "complex" else "LIG Water_and_ions"
    return f"""\
; ABFE FEP  compound={name}  leg={leg}  window={window}
; lambda: coul={COUL[window]:.2f}  vdw={VDW[window]:.2f}
integrator           = md
nsteps               = 750000
dt                   = 0.002
nstxout-compressed   = 5000
nstenergy            = 500
nstlog               = 5000
nstdhdl              = 100

cutoff-scheme        = Verlet
nstlist              = 10
coulombtype          = PME
rcoulomb             = 1.0
rvdw                 = 1.0
pbc                  = xyz
DispCorr             = EnerPres

tcoupl               = V-rescale
tc-grps              = {tc_grps}
tau_t                = 0.1   0.1
ref_t                = 300   300

pcoupl               = Parrinello-Rahman
pcoupltype           = isotropic
tau_p                = 2.0
ref_p                = 1.0
compressibility      = 4.5e-5

constraints          = h-bonds
constraint_algorithm = LINCS
lincs_iter           = 1
lincs_order          = 4

gen_vel              = yes
gen_temp             = 300
gen_seed             = {42 + window + (100 if leg == 'solvent' else 0)}
continuation         = no

; FEP settings
free-energy          = yes
couple-moltype       = LIG
couple-lambda0       = vdw-q
couple-lambda1       = none
couple-intramol      = no
init-lambda-state    = {window}
coul-lambdas         = {COUL_STR}
vdw-lambdas          = {VDW_STR}
sc-alpha             = 0.5
sc-power             = 1
sc-sigma             = 0.3
sc-coul              = no
calc-lambda-neighbors = -1
dhdl-print-energy    = total
"""

for name in BP:
    md_dir = f"{BASE}/md_{name}"
    for leg in ("complex", "solvent"):
        leg_dir = f"{md_dir}/abfe_{leg}_mdps"
        os.makedirs(leg_dir, exist_ok=True)
        for w in range(N_WIN):
            with open(f"{leg_dir}/win{w:02d}.mdp", "w") as f:
                f.write(fep_mdp(w, leg, name))
    print(f"  {name}: {N_WIN}×2 MDP files written")

print("\nSteps 3–5 done.")
