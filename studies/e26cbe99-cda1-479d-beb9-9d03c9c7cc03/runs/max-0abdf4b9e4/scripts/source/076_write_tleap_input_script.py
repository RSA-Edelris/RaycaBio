
import subprocess, os

# ── Write tleap input script ───────────────────────────────────────────────
tleap_in = f"""\
source leaprc.protein.ff14SB
source leaprc.gaff2
source leaprc.water.tip3p

LIG = loadmol2 {lig_mol2}
loadamberparams {lig_frcmod}

REC = loadpdb {rec_tleap}
complex = combine {{ REC LIG }}

check complex

solvateBox complex TIP3PBOX 12.0
addIons complex Na+ 0
addIons complex Cl- 0
addIons2 complex Na+ 0.15

savepdb complex {MD_DIR}/complex_solvated.pdb
saveamberparm complex {MD_DIR}/complex.prmtop {MD_DIR}/complex.inpcrd

quit
"""

tleap_script = f'{MD_DIR}/tleap.in'
with open(tleap_script, 'w') as fh:
    fh.write(tleap_in)

print("Running tleap (solvation + parameterization)...")
r = subprocess.run(['tleap', '-f', tleap_script],
                   capture_output=True, text=True, cwd=MD_DIR)

# Show last 40 lines (summary + any errors)
output_lines = (r.stdout + r.stderr).splitlines()
for line in output_lines[-40:]:
    print(line)

# Check key outputs
for fname in ['complex.prmtop', 'complex.inpcrd']:
    path = f'{MD_DIR}/{fname}'
    exists = os.path.exists(path)
    sz = os.path.getsize(path) if exists else 0
    print(f"\n{fname}: {'OK' if exists else 'MISSING'} ({sz:,} bytes)")
