
import tempfile, os

tmpdir2 = tempfile.mkdtemp(prefix='tleap2_')
prmtop2 = os.path.join(tmpdir2, 'receptor.prmtop')
inpcrd2 = os.path.join(tmpdir2, 'receptor.inpcrd')
leapin2 = os.path.join(tmpdir2, 'leap_rec.in')

with open(leapin2, 'w') as fh:
    fh.write(f"source leaprc.protein.ff14SB\n"
             f"REC = loadpdb {FIXED_PDB}\n"
             f"saveamberparm REC {prmtop2} {inpcrd2}\n"
             f"quit\n")

r = subprocess.run(
    ['tleap', '-f', leapin2],
    capture_output=True, text=True, cwd=tmpdir2,
    env={**os.environ, 'AMBERHOME': AMBER_HOME}
)
print("Return code:", r.returncode)
# Show only warnings/errors/fatals
for line in r.stdout.splitlines():
    if any(x in line for x in ['Warning', 'Fatal', 'FATAL', 'Error', 'ERROR', 'prmtop', 'Exiting']):
        print(line)
print("prmtop exists:", os.path.exists(prmtop2), 
      "| size:", os.path.getsize(prmtop2) if os.path.exists(prmtop2) else 0)
