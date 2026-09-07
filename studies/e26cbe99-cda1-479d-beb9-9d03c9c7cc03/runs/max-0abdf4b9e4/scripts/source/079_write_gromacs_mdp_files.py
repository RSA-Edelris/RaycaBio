
import os

# ── Write GROMACS MDP files ────────────────────────────────────────────────

# Energy minimisation
em_mdp = """\
; Energy minimisation
integrator      = steep
nsteps          = 10000
emtol           = 100.0
emstep          = 0.01
nstlist         = 10
cutoff-scheme   = Verlet
ns_type         = grid
coulombtype     = PME
rcoulomb        = 1.0
rvdw            = 1.0
pbc             = xyz
DispCorr        = EnerPres
"""

# NPT equilibration (200 ps)
npt_eq_mdp = """\
; NPT equilibration 200 ps
integrator      = md
nsteps          = 100000
dt              = 0.002
nstxout         = 5000
nstvout         = 5000
nstenergy       = 5000
nstlog          = 5000
cutoff-scheme   = Verlet
ns_type         = grid
nstlist         = 10
coulombtype     = PME
rcoulomb        = 1.0
rvdw            = 1.0
pbc             = xyz
DispCorr        = EnerPres
tcoupl          = V-rescale
tc-grps         = Protein_LIG Water_and_ions
tau_t           = 0.1   0.1
ref_t           = 300   300
pcoupl          = Berendsen
pcoupltype      = isotropic
tau_p           = 2.0
ref_p           = 1.0
compressibility = 4.5e-5
constraints     = h-bonds
constraint_algorithm = LINCS
lincs_iter      = 1
lincs_order     = 4
gen_vel         = yes
gen_temp        = 300
gen_seed        = 42
"""

# 10 ns NPT production
prod_mdp = """\
; 10 ns NPT production
integrator      = md
nsteps          = 5000000
dt              = 0.002
nstxout-compressed = 5000
nstvout         = 0
nstenergy       = 5000
nstlog          = 5000
cutoff-scheme   = Verlet
ns_type         = grid
nstlist         = 10
coulombtype     = PME
rcoulomb        = 1.0
rvdw            = 1.0
pbc             = xyz
DispCorr        = EnerPres
tcoupl          = V-rescale
tc-grps         = Protein_LIG Water_and_ions
tau_t           = 0.1   0.1
ref_t           = 300   300
pcoupl          = Parrinello-Rahman
pcoupltype      = isotropic
tau_p           = 2.0
ref_p           = 1.0
compressibility = 4.5e-5
constraints     = h-bonds
constraint_algorithm = LINCS
lincs_iter      = 1
lincs_order     = 4
gen_vel         = no
continuation    = yes
"""

for fname, content in [('em.mdp', em_mdp), ('npt_eq.mdp', npt_eq_mdp), ('prod.mdp', prod_mdp)]:
    with open(f'{MD_DIR}/{fname}', 'w') as fh:
        fh.write(content)
    print(f"Written: {fname}")

# ── Check what GROMACS groups are available in this topology ──────────────
import subprocess
r = subprocess.run(
    ['gmx', 'make_ndx', '-f', f'{MD_DIR}/complex.gro', '-o', f'{MD_DIR}/index.ndx'],
    input='q\n', capture_output=True, text=True
)
# Extract group list
for line in r.stdout.splitlines():
    if line.strip().startswith('Group') or (line.strip() and line.strip()[0].isdigit()):
        print(line)
