
import subprocess, os
import parmed as pmd

# ======================================================================
# Step 3: Convert solvent-leg prmtop → GROMACS top + gro (ParmEd)
# ======================================================================
print("=== Step 3: ParmEd conversion for solvent leg ===")
for name in BP:
    md_dir  = f"{BASE}/md_{name}"
    sv_dir  = f"{md_dir}/abfe_solv"
    prmtop  = f"{sv_dir}/lig_solv.prmtop"
    inpcrd  = f"{sv_dir}/lig_solv.inpcrd"
    top_out = f"{sv_dir}/lig_solv.top"
    gro_out = f"{sv_dir}/lig_solv.gro"

    if os.path.exists(top_out) and os.path.exists(gro_out):
        print(f"  {name}: already converted, skipping")
        continue

    struct = pmd.load_file(prmtop, inpcrd)
    struct.save(top_out, overwrite=True)
    struct.save(gro_out, overwrite=True)
    n_atoms = len(struct.atoms)
    print(f"  {name}: lig_solv.top + lig_solv.gro ({n_atoms} atoms)")

# ======================================================================
# Step 4: Generate modified complex.top with Boresch restraints
# ======================================================================
print("\n=== Step 4: Add Boresch restraints to complex.top ===")

def boresch_section(p):
    r1,r2,r3 = p['r1'], p['r2'], p['r3']
    l1,l2,l3 = p['l1'], p['l2'], p['l3']
    r0 = p['r0']
    tA, tB = p['tA'], p['tB']
    pA, pB, pC = p['pA'], p['pB'], p['pC']
    lines = [
        "",
        "[ intermolecular_interactions ]",
        "; Boresch 6-DOF restraints: always ON in both lambda states",
        "; Force constants: k_r=4184 kJ/mol/nm², k_a=k_d=41.84 kJ/mol/rad²",
        "[ bonds ]",
        f"; ai    aj   funct  b0_A(nm)     kb_A        b0_B(nm)     kb_B",
        f"  {r1:5d} {l1:5d}   1     {r0:.4f}     {K_B:.1f}     {r0:.4f}     {K_B:.1f}",
        "[ angles ]",
        f"; ai    aj    ak   funct  theta0_A  ktheta_A  theta0_B  ktheta_B",
        f"  {r2:5d} {r1:5d} {l1:5d}   1     {tA:.2f}     {K_A:.2f}     {tA:.2f}     {K_A:.2f}",
        f"  {r1:5d} {l1:5d} {l2:5d}   1     {tB:.2f}     {K_A:.2f}     {tB:.2f}     {K_A:.2f}",
        "[ dihedrals ]",
        f"; ai    aj    ak    al   funct  phi0_A  kphi_A  phi0_B  kphi_B",
        f"  {r3:5d} {r2:5d} {r1:5d} {l1:5d}   2     {pA:.2f}     {K_A:.2f}     {pA:.2f}     {K_A:.2f}",
        f"  {r2:5d} {r1:5d} {l1:5d} {l2:5d}   2     {pB:.2f}     {K_A:.2f}     {pB:.2f}     {K_A:.2f}",
        f"  {r1:5d} {l1:5d} {l2:5d} {l3:5d}   2     {pC:.2f}     {K_A:.2f}     {pC:.2f}     {K_A:.2f}",
    ]
    return "\n".join(lines) + "\n"

for name, p in BP.items():
    md_dir   = f"{BASE}/md_{name}"
    top_in   = f"{md_dir}/complex.top"
    top_out  = f"{md_dir}/complex_abfe.top"

    if os.path.exists(top_out):
        print(f"  {name}: complex_abfe.top already exists, skipping")
        continue

    with open(top_in) as f:
        content = f.read()

    # Append Boresch section after [ molecules ] block (end of file)
    content += boresch_section(p)

    with open(top_out, "w") as f:
        f.write(content)

    print(f"  {name}: wrote complex_abfe.top (Boresch r1={p['r1']},l1={p['l1']})")

# ======================================================================
# Step 5: Write FEP MDP files (complex and solvent legs)
# ======================================================================
print("\n=== Step 5: Write FEP MDP files ===")

COMPLEX_MDP_TEMPLATE = """\
; ABFE FEP window {window} — complex leg
; lambda: coul={coul:.2f}  vdw={vdw:.2f}
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
tc-grps              = Protein_LIG Water_and_ions
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
gen_seed             = {seed}
continuation         = no

; FEP settings
free-energy          = yes
couple-moltype       = LIG
couple-lambda0       = vdw-q
couple-lambda1       = none
couple-intramol      = no
init-lambda-state    = {window}

coul-lambdas         = {coul_str}
vdw-lambdas          = {vdw_str}

sc-alpha             = 0.5
sc-power             = 1
sc-sigma             = 0.3
sc-coul              = no

calc-lambda-neighbors = -1
dhdl-print-energy    = total
"""

SOLVENT_MDP_TEMPLATE = """\
; ABFE FEP window {window} — solvent leg
; lambda: coul={coul:.2f}  vdw={vdw:.2f}
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
tc-grps              = LIG Water_and_ions
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
gen_seed             = {seed}
continuation         = no

; FEP settings
free-energy          = yes
couple-moltype       = LIG
couple-lambda0       = vdw-q
couple-lambda1       = none
couple-intramol      = no
init-lambda-state    = {window}

coul-lambdas         = {coul_str}
vdw-lambdas          = {vdw_str}

sc-alpha             = 0.5
sc-power             = 1
sc-sigma             = 0.3
sc-coul              = no

calc-lambda-neighbors = -1
dhdl-print-energy    = total
"""

for name, p in BP.items():
    md_dir = f"{BASE}/md_{name}"

    # Complex leg MDPs
    cx_dir = f"{md_dir}/abfe_complex_mdps"
    os.makedirs(cx_dir, exist_ok=True)
    for w in range(N_WIN):
        fn = f"{cx_dir}/fep_complex_win{w:02d}.mdp"
        content = COMPLEX_MDP_TEMPLATE.format(
            window=w, coul=COUL[w], vdw=VDW[w],
            coul_str=COUL_STR, vdw_str=VDW_STR,
            seed=42 + w)
        with open(fn, "w") as f:
            f.write(content)

    # Solvent leg MDPs
    sv_dir_mdp = f"{md_dir}/abfe_solv_mdps"
    os.makedirs(sv_dir_mdp, exist_ok=True)
    for w in range(N_WIN):
        fn = f"{sv_dir_mdp}/fep_solvent_win{w:02d}.mdp"
        content = SOLVENT_MDP_TEMPLATE.format(
            window=w, coul=COUL[w], vdw=VDW[w],
            coul_str=COUL_STR, vdw_str=VDW_STR,
            seed=142 + w)
        with open(fn, "w") as f:
            f.write(content)

    print(f"  {name}: {N_WIN} complex MDPs + {N_WIN} solvent MDPs written")

print("\nSteps 3-5 complete.")
