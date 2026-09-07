
# ── MMPBSA input file ──────────────────────────────────────────────────────
mmpbsa_in = """\
Per-residue MM-GBSA for CRBN pocket + EDS01806218_ent2
&general
  startframe = 200,        ! skip first 2 ns (1 ns eq + 1 ns warmup)
  endframe   = 1000,       ! last frame (10 ns, 1000 frames at 10 ps/frame)
  interval   = 4,          ! every 4th frame -> 200 frames analyzed
  verbose    = 2,          ! print all energies
  keep_files = 0,
/
&gb
  igb      = 5,            ! OBC2 (Onufriev-Bashford-Case) GB model
  saltcon  = 0.15,         ! 150 mM NaCl
/
"""

# ── cpptraj strip script to convert xtc -> NetCDF (no solvent) ──────────
cpptraj_strip = """\
# Strip solvent from GROMACS trajectory for MMPBSA
parm {md}/complex.prmtop
trajin {md}/prod.xtc
strip :WAT,Cl-
trajout {md}/prod_nowater.nc netcdf
run
quit
""".format(md=MD_DIR)

# ── Complete analysis script ───────────────────────────────────────────────
analysis_script = """\
#!/usr/bin/env bash
# Run when prod.xtc has been retrieved from Isambard
set -e
MD={md}
AMBERHOME=/home/ubuntu/rayca-runtime/.mamba/envs/rayca
export AMBERHOME

echo "=== Step 1: Strip solvent from trajectory ==="
cpptraj -i $MD/cpptraj_strip.in

echo "=== Step 2: Run MMPBSA.py ==="
$AMBERHOME/bin/MMPBSA.py -O \\
  -i  $MD/mmpbsa.in \\
  -o  $MD/mmpbsa_results.dat \\
  -do $MD/mmpbsa_decomp.dat \\
  -sp $MD/complex.prmtop \\
  -cp $MD/complex_nowater.prmtop \\
  -rp $MD/receptor.prmtop \\
  -lp $MD/ligand.prmtop \\
  -y  $MD/prod_nowater.nc

echo "=== Results ==="
grep -A5 "DELTA TOTAL" $MD/mmpbsa_results.dat || true
""".format(md=MD_DIR)

# Write files
for fname, content in [
    (f'{MD_DIR}/mmpbsa.in',          mmpbsa_in),
    (f'{MD_DIR}/cpptraj_strip.in',   cpptraj_strip),
    (f'{MD_DIR}/run_mmpbsa.sh',      analysis_script),
]:
    with open(fname, 'w') as fh:
        fh.write(content)
    print(f"Written: {fname.split('/')[-1]}")

import subprocess
subprocess.run(['chmod', '+x', f'{MD_DIR}/run_mmpbsa.sh'])
print("\nAnalysis pipeline ready. Waiting for trajectory from Isambard (job 6284357).")
print(f"Once prod.xtc arrives in {MD_DIR}, run: bash {MD_DIR}/run_mmpbsa.sh")
