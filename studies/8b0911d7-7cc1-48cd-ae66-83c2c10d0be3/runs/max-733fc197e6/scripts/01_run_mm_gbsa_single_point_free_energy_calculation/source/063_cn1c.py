
import tempfile, os, subprocess
from rdkit import Chem
from rdkit.Chem import AllChem

AMBER_HOME = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
LIG_DIR = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/ligands'

smiles16 = 'Cn1c(CN2CC3(CC3)C[C@@H]2c2cccc(C(=O)NC3CCC3)n2)nc2ccccc21'

mol = Chem.MolFromSmiles(smiles16)
mol = Chem.AddHs(mol)
AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
AllChem.MMFFOptimizeMolecule(mol)

tmpdir3 = tempfile.mkdtemp(prefix='lig16_')
sdf_path = os.path.join(tmpdir3, 'cpd16r.sdf')
mol2_path = os.path.join(tmpdir3, 'cpd16r.mol2')

w = Chem.SDWriter(sdf_path)
w.write(mol)
w.close()
print(f"SDF written: {sdf_path}")
print(f"Mol atoms: {mol.GetNumAtoms()}, heavy: {sum(1 for a in mol.GetAtoms() if a.GetAtomicNum()!=1)}")

env = {**os.environ, 'AMBERHOME': AMBER_HOME}
r = subprocess.run([
    'antechamber',
    '-i', sdf_path, '-fi', 'sdf',
    '-o', mol2_path, '-fo', 'mol2',
    '-c', 'bcc', '-nc', '0',
    '-at', 'gaff2', '-s', '2', '-pf', 'y',
], capture_output=True, text=True, cwd=tmpdir3, env=env)

print("Return code:", r.returncode)
print("STDOUT:", r.stdout[-1500:])
print("STDERR:", r.stderr[-500:])

# Check for sqm.out
sqm_out = os.path.join(tmpdir3, 'sqm.out')
if os.path.exists(sqm_out):
    with open(sqm_out) as fh:
        print("\nsqm.out (last 40 lines):")
        lines = fh.readlines()
        print(''.join(lines[-40:]))
else:
    print("sqm.out not found")
    print("Files in tmpdir:", os.listdir(tmpdir3))
