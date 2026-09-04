
import tempfile, os, subprocess

AMBER_HOME = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'

# Write a small test script to run antechamber for Cpd16 R
test_script = '''
import tempfile, os, subprocess
from rdkit import Chem
from rdkit.Chem import AllChem

AMBER_HOME = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca"
smiles16 = "Cn1c(CN2CC3(CC3)C[C@@H]2c2cccc(C(=O)NC3CCC3)n2)nc2ccccc21"

mol = Chem.MolFromSmiles(smiles16)
mol = Chem.AddHs(mol)
AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
AllChem.MMFFOptimizeMolecule(mol)

tmpdir = tempfile.mkdtemp(prefix="lig16_")
sdf = os.path.join(tmpdir, "cpd16r.sdf")
mol2 = os.path.join(tmpdir, "cpd16r.mol2")

w = Chem.SDWriter(sdf)
w.write(mol)
w.close()
print(f"SDF: {sdf}")

env = {**os.environ, "AMBERHOME": AMBER_HOME}
r = subprocess.run([
    "antechamber", "-i", sdf, "-fi", "sdf",
    "-o", mol2, "-fo", "mol2",
    "-c", "bcc", "-nc", "0", "-at", "gaff2", "-s", "2", "-pf", "y",
], capture_output=True, text=True, cwd=tmpdir, env=env, timeout=300)

print("rc:", r.returncode)
print("stdout:", r.stdout[-2000:])
print("stderr:", r.stderr[-500:])

sqm = os.path.join(tmpdir, "sqm.out")
if os.path.exists(sqm):
    with open(sqm) as f:
        lines = f.readlines()
    print("sqm.out tail:\\n" + "".join(lines[-30:]))
else:
    print("no sqm.out; files:", os.listdir(tmpdir))
'''

with open('/tmp/test_antechamber16.py', 'w') as f:
    f.write(test_script)

r = subprocess.run(
    ['/home/ubuntu/rayca-runtime/.venv/bin/python3', '/tmp/test_antechamber16.py'],
    capture_output=True, text=True, timeout=400
)
print(r.stdout[-3000:])
print(r.stderr[-1000:])
