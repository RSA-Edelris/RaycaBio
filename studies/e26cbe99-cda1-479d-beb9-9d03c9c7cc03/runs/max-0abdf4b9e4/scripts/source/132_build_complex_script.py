
import os

BASE = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"
GMX = "/projects/u6sp/software-aarch64/gromacs-2026.1-mpi/bin/gmx_mpi"
CLUSTER = "own:7738ec0ba2c5bbae"

def build_complex_script(name):
    return f"""#!/bin/bash
set -euo pipefail
echo "=== ABFE complex leg: {name} ==="
GMX={GMX}
WDIR=$(mktemp -d)
echo "Working dir: $WDIR"

cp $RAYCA_INPUTS/md_{name}/abfe_start.gro  $WDIR/start.gro
cp $RAYCA_INPUTS/md_{name}/complex_abfe.top $WDIR/complex.top
cp $RAYCA_INPUTS/md_{name}/index.ndx        $WDIR/index.ndx
for w in $(seq -f "%02g" 0 16); do
  cp $RAYCA_INPUTS/md_{name}/abfe_complex_mdps/win${{w}}.mdp $WDIR/win${{w}}.mdp
done

cd $WDIR

for w in $(seq -f "%02g" 0 16); do
  echo "--- Complex window $w (coul/vdw from MDP) ---"
  mkdir -p win${{w}}
  $GMX grompp -f win${{w}}.mdp -c start.gro -p complex.top \\
              -n index.ndx -o win${{w}}/fep.tpr -maxwarn 20
  $GMX mdrun -s win${{w}}/fep.tpr -deffnm win${{w}}/fep \\
             -dhdl win${{w}}/dhdl.xvg \\
             -ntomp 8 -nb gpu -pme gpu -ntmpi 1 -v
  cp win${{w}}/dhdl.xvg $RAYCA_OUT/complex_{name}_win${{w}}_dhdl.xvg
  echo "Window $w done"
done

echo "=== Complex leg complete for {name} ==="
"""

def build_solvent_script(name):
    return f"""#!/bin/bash
set -euo pipefail
echo "=== ABFE solvent leg: {name} ==="
GMX={GMX}
WDIR=$(mktemp -d)
echo "Working dir: $WDIR"

cp $RAYCA_INPUTS/md_{name}/abfe_solv/lig_solv.gro $WDIR/lig.gro
cp $RAYCA_INPUTS/md_{name}/abfe_solv/lig_solv.top $WDIR/lig.top
for w in $(seq -f "%02g" 0 16); do
  cp $RAYCA_INPUTS/md_{name}/abfe_solvent_mdps/win${{w}}.mdp $WDIR/win${{w}}.mdp
done

cd $WDIR

# EM
cat > em.mdp << 'EOFMDP'
integrator = steep
emtol = 200.0
nsteps = 5000
nstxout = 0
nstenergy = 1000
nstlog = 5000
cutoff-scheme = Verlet
nstlist = 10
coulombtype = PME
rcoulomb = 1.0
rvdw = 1.0
pbc = xyz
DispCorr = EnerPres
constraints = none
EOFMDP

$GMX grompp -f em.mdp -c lig.gro -p lig.top -o em.tpr -maxwarn 20
$GMX mdrun -s em.tpr -deffnm em -ntomp 8 -nb gpu -pme cpu -ntmpi 1 -v
echo "EM done"

# NPT equilibration
cat > npt_eq.mdp << 'EOFMDP'
integrator = md
nsteps = 100000
dt = 0.002
nstxout = 0
nstenergy = 5000
nstlog = 10000
cutoff-scheme = Verlet
nstlist = 10
coulombtype = PME
rcoulomb = 1.0
rvdw = 1.0
pbc = xyz
DispCorr = EnerPres
tcoupl = V-rescale
tc-grps = System
tau_t = 0.1
ref_t = 300
pcoupl = Berendsen
pcoupltype = isotropic
tau_p = 2.0
ref_p = 1.0
compressibility = 4.5e-5
constraints = h-bonds
constraint_algorithm = LINCS
lincs_iter = 1
lincs_order = 4
gen_vel = yes
gen_temp = 300
gen_seed = 99
EOFMDP

$GMX grompp -f npt_eq.mdp -c em.gro -p lig.top -o npt_eq.tpr -maxwarn 20
$GMX mdrun -s npt_eq.tpr -deffnm npt_eq -ntomp 8 -nb gpu -pme gpu -ntmpi 1 -v
echo "NPT eq done"

# FEP windows
for w in $(seq -f "%02g" 0 16); do
  echo "--- Solvent window $w ---"
  mkdir -p win${{w}}
  $GMX grompp -f win${{w}}.mdp -c npt_eq.gro -p lig.top \\
              -o win${{w}}/fep.tpr -maxwarn 20
  $GMX mdrun -s win${{w}}/fep.tpr -deffnm win${{w}}/fep \\
             -dhdl win${{w}}/dhdl.xvg \\
             -ntomp 8 -nb gpu -pme gpu -ntmpi 1 -v
  cp win${{w}}/dhdl.xvg $RAYCA_OUT/solvent_{name}_win${{w}}_dhdl.xvg
  echo "Solvent window $w done"
done

echo "=== Solvent leg complete for {name} ==="
"""

# Build input lists
def complex_inputs(name):
    inputs = [
        f"md_{name}/abfe_start.gro",
        f"md_{name}/complex_abfe.top",
        f"md_{name}/index.ndx",
    ]
    for w in range(N_WIN):
        inputs.append(f"md_{name}/abfe_complex_mdps/win{w:02d}.mdp")
    return inputs

def solvent_inputs(name):
    inputs = [
        f"md_{name}/abfe_solv/lig_solv.gro",
        f"md_{name}/abfe_solv/lig_solv.top",
    ]
    for w in range(N_WIN):
        inputs.append(f"md_{name}/abfe_solvent_mdps/win{w:02d}.mdp")
    return inputs

# Print summary
for name in BP:
    print(f"\n{name}:")
    print(f"  Complex inputs: {len(complex_inputs(name))} files")
    print(f"  Solvent inputs: {len(solvent_inputs(name))} files")

# Store for next cell
scripts = {}
for name in BP:
    scripts[name] = {
        "complex_script": build_complex_script(name),
        "solvent_script": build_solvent_script(name),
        "complex_inputs": complex_inputs(name),
        "solvent_inputs": solvent_inputs(name),
    }
print("\nScripts generated, ready to submit.")
