
import os, re

MD = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d/md_prep'
INP = f'{MD}/inputs'

# ─── MDP files ───────────────────────────────────────────────────────────────

EM_MDP = """\
; Energy minimisation
integrator  = steep
emtol       = 100.0
emstep      = 0.01
nsteps      = 50000
nstlist     = 10
cutoff-scheme = Verlet
ns_type     = grid
coulombtype = PME
rcoulomb    = 1.0
rvdw        = 1.0
pbc         = xyz
"""

NVT_MDP = """\
; NVT equilibration — 100 ps with protein+ligand position restraints
define      = -DPOSRES
integrator  = md
nsteps      = 50000        ; 100 ps
dt          = 0.002
nstlog      = 500
nstenergy   = 500
nstxout-compressed = 500
constraint_algorithm = lincs
constraints = h-bonds
lincs_iter  = 1
lincs_order = 4
cutoff-scheme = Verlet
nstlist     = 10
ns_type     = grid
coulombtype = PME
rcoulomb    = 1.0
rvdw        = 1.0
tcoupl      = V-rescale
tc-grps     = Protein_LIG   Water_and_ions
tau_t       = 0.1           0.1
ref_t       = 300           300
pcoupl      = no
pbc         = xyz
gen_vel     = yes
gen_temp    = 300
gen_seed    = SEED
"""

NPT_MDP = """\
; NPT equilibration — 500 ps with protein+ligand position restraints
define      = -DPOSRES
integrator  = md
nsteps      = 250000       ; 500 ps
dt          = 0.002
nstlog      = 500
nstenergy   = 500
nstxout-compressed = 500
constraint_algorithm = lincs
constraints = h-bonds
lincs_iter  = 1
lincs_order = 4
cutoff-scheme = Verlet
nstlist     = 10
ns_type     = grid
coulombtype = PME
rcoulomb    = 1.0
rvdw        = 1.0
tcoupl      = V-rescale
tc-grps     = Protein_LIG   Water_and_ions
tau_t       = 0.1           0.1
ref_t       = 300           300
pcoupl      = Parrinello-Rahman
pcoupltype  = isotropic
tau_p       = 2.0
ref_p       = 1.0
compressibility = 4.5e-5
pbc         = xyz
gen_vel     = no
continuation = yes
"""

PROD_MDP = """\
; Production MD — 20 ns
integrator  = md
nsteps      = 10000000     ; 20 ns at 2 fs
dt          = 0.002
nstlog      = 5000
nstenergy   = 5000
nstxout-compressed = 5000  ; save every 10 ps
compressed-x-grps  = Protein_LIG
constraint_algorithm = lincs
constraints = h-bonds
lincs_iter  = 1
lincs_order = 4
cutoff-scheme = Verlet
nstlist     = 10
ns_type     = grid
coulombtype = PME
rcoulomb    = 1.0
rvdw        = 1.0
tcoupl      = V-rescale
tc-grps     = Protein_LIG   Water_and_ions
tau_t       = 0.1           0.1
ref_t       = 300           300
pcoupl      = Parrinello-Rahman
pcoupltype  = isotropic
tau_p       = 2.0
ref_p       = 1.0
compressibility = 4.5e-5
pbc         = xyz
gen_vel     = no
continuation = yes
"""

for fname, content in [('em.mdp', EM_MDP), ('nvt.mdp', NVT_MDP),
                        ('npt.mdp', NPT_MDP), ('md.mdp', PROD_MDP)]:
    with open(f'{INP}/{fname}', 'w') as f:
        f.write(content)
    print(f'Written: {fname}')

print("MDP files done")
