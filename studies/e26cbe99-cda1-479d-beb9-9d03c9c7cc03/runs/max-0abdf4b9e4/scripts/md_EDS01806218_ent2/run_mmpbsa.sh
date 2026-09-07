#!/usr/bin/env bash
# Run when prod.xtc has been retrieved from Isambard
set -e
MD=/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85/md_EDS01806218_ent2
AMBERHOME=/home/ubuntu/rayca-runtime/.mamba/envs/rayca
export AMBERHOME

echo "=== Step 1: Strip solvent from trajectory ==="
cpptraj -i $MD/cpptraj_strip.in

echo "=== Step 2: Run MMPBSA.py ==="
$AMBERHOME/bin/MMPBSA.py -O \
  -i  $MD/mmpbsa.in \
  -o  $MD/mmpbsa_results.dat \
  -do $MD/mmpbsa_decomp.dat \
  -sp $MD/complex.prmtop \
  -cp $MD/complex_nowater.prmtop \
  -rp $MD/receptor.prmtop \
  -lp $MD/ligand.prmtop \
  -y  $MD/prod_nowater.nc

echo "=== Results ==="
grep -A5 "DELTA TOTAL" $MD/mmpbsa_results.dat || true
