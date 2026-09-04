
import subprocess, os, tempfile

RECEPTOR_PDB = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/9C56_receptor.pdb'
AMBER_HOME   = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'

tmpdir = tempfile.mkdtemp(prefix='tleap_test_')
prmtop = os.path.join(tmpdir, 'receptor.prmtop')
inpcrd = os.path.join(tmpdir, 'receptor.inpcrd')
leapin = os.path.join(tmpdir, 'leap_rec.in')

with open(leapin, 'w') as f:
    f.write(f"source leaprc.protein.ff14SB\n"
            f"REC = loadpdb {RECEPTOR_PDB}\n"
            f"saveamberparm REC {prmtop} {inpcrd}\n"
            f"quit\n")

r = subprocess.run(
    ['tleap', '-f', leapin],
    capture_output=True, text=True,
    cwd=tmpdir,
    env={**os.environ, 'AMBERHOME': AMBER_HOME}
)

print("Return code:", r.returncode)
print("\n--- STDOUT ---")
print(r.stdout[-4000:])
print("\n--- STDERR ---")
print(r.stderr[-1000:])
print("\nFiles created:", os.listdir(tmpdir))
