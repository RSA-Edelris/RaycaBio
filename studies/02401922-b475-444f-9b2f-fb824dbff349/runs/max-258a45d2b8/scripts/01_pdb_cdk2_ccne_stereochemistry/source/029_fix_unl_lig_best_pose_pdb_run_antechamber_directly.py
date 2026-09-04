
# Fix UNL→LIG in best_pose.pdb, then run antechamber directly on docked pose
with open('best_pose.pdb') as f:
    pdb_content = f.read()
pdb_fixed = pdb_content.replace('UNL', 'LIG')
with open('best_pose_lig.pdb','w') as f:
    f.write(pdb_fixed)
print("best_pose_lig.pdb written (UNL→LIG)")

# Run antechamber on the docked pose PDB with net charge +1
r_ac2 = subprocess.run([
    'antechamber',
    '-i', 'best_pose_lig.pdb', '-fi', 'pdb',
    '-o', 'ligand_docked.mol2', '-fo', 'mol2',
    '-c', 'bcc',
    '-nc', '1',
    '-at', 'gaff2',
    '-rn', 'LIG',
    '-dr', 'n'
], capture_output=True, text=True, cwd=WS)

print("antechamber rc:", r_ac2.returncode)
if r_ac2.returncode == 0:
    sz = os.path.getsize(f'{WS}/ligand_docked.mol2')
    print(f"ligand_docked.mol2: {sz} bytes")
else:
    print("STDOUT:", r_ac2.stdout[-800:])
    print("STDERR:", r_ac2.stderr[-300:])
