
import os

INP = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d/md_prep/inputs'

# Update NVT/NPT/Production MDPs to use Protein + non-Protein (ligand rides with solvent)
# This avoids needing a custom Protein_LIG index group, which is hard to create non-interactively
NVT_MDP = """\
; NVT equilibration — 100 ps, position restraints on protein + ligand
define      = -DPOSRES
integrator  = md
nsteps      = 50000
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
coulombtype = PME
rcoulomb    = 1.0
rvdw        = 1.0
rvdw-switch = 0.0
tcoupl      = V-rescale
tc-grps     = Protein   non-Protein
tau_t       = 0.1        0.1
ref_t       = 300        300
pcoupl      = no
pbc         = xyz
gen_vel     = yes
gen_temp    = 300
gen_seed    = SEED
"""

NPT_MDP = """\
; NPT equilibration — 500 ps, position restraints on protein + ligand
define      = -DPOSRES
integrator  = md
nsteps      = 250000
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
coulombtype = PME
rcoulomb    = 1.0
rvdw        = 1.0
tcoupl      = V-rescale
tc-grps     = Protein   non-Protein
tau_t       = 0.1        0.1
ref_t       = 300        300
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
; Production MD — 20 ns (10 M steps at 2 fs)
integrator  = md
nsteps      = 10000000
dt          = 0.002
nstlog      = 5000
nstenergy   = 5000
nstxout-compressed = 5000
compressed-x-grps  = System
constraint_algorithm = lincs
constraints = h-bonds
lincs_iter  = 1
lincs_order = 4
cutoff-scheme = Verlet
nstlist     = 10
coulombtype = PME
rcoulomb    = 1.0
rvdw        = 1.0
tcoupl      = V-rescale
tc-grps     = Protein   non-Protein
tau_t       = 0.1        0.1
ref_t       = 300        300
pcoupl      = Parrinello-Rahman
pcoupltype  = isotropic
tau_p       = 2.0
ref_p       = 1.0
compressibility = 4.5e-5
pbc         = xyz
gen_vel     = no
continuation = yes
"""

for fname, content in [('nvt.mdp', NVT_MDP), ('npt.mdp', NPT_MDP), ('md.mdp', PROD_MDP)]:
    with open(f'{INP}/{fname}', 'w') as f:
        f.write(content)
print("Updated mdp files written")

# ── Python helper script to create analysis index file ──────────────────────
# Runs on Isambard with /opt/cray/pe/python/3.11.7/bin/python3
# Knows: ChainA = first 4859 protein atoms, ChainB = next 4375, LIG follows
CREATE_NDX = '''\
#!/usr/bin/env python3
"""Create GROMACS index file for analysis groups from a solvated .gro file."""
import sys, os

gro = sys.argv[1]
ndx = sys.argv[2]
cid = sys.argv[3]          # compound ID = ligand mol name in topology

CHAIN_A_ATOMS = 4859       # from pdb2gmx output
CHAIN_B_ATOMS = 4375

# Parse gro file
with open(gro) as f:
    f.readline()           # title
    n = int(f.readline())
    atoms = []
    for _ in range(n):
        line = f.readline()
        resname = line[5:10].strip()
        atoms.append(resname)

chain_a  = list(range(1, CHAIN_A_ATOMS + 1))
chain_b  = list(range(CHAIN_A_ATOMS + 1, CHAIN_A_ATOMS + CHAIN_B_ATOMS + 1))
lig_idx  = [i + 1 for i, r in enumerate(atoms) if r == "MOL"]
wat_idx  = [i + 1 for i, r in enumerate(atoms) if r == "SOL"]
ion_idx  = [i + 1 for i, r in enumerate(atoms) if r in ("NA", "CL")]
prot_idx = chain_a + chain_b

def write_grp(fh, name, indices):
    fh.write(f"[ {name} ]\\n")
    for j, idx in enumerate(indices):
        fh.write(f" {idx}")
        if (j + 1) % 15 == 0:
            fh.write("\\n")
    fh.write("\\n\\n")

with open(ndx, "w") as fh:
    write_grp(fh, "System",        list(range(1, n + 1)))
    write_grp(fh, "Protein",       prot_idx)
    write_grp(fh, "ChainA_CDK2",   chain_a)
    write_grp(fh, "ChainB_CyclinE", chain_b)
    write_grp(fh, "LIG",           lig_idx)
    write_grp(fh, "Protein_LIG",   prot_idx + lig_idx)
    write_grp(fh, "Water",         wat_idx)
    write_grp(fh, "Ion",           ion_idx)
    write_grp(fh, "Water_and_ions", wat_idx + ion_idx)
    write_grp(fh, "non_Protein",   lig_idx + wat_idx + ion_idx)

print(f"Index written: {ndx}  ({len(chain_a)} A, {len(chain_b)} B, {len(lig_idx)} LIG atoms)")
'''

with open(f'{INP}/create_ndx.py', 'w') as f:
    f.write(CREATE_NDX)
print("create_ndx.py written")
