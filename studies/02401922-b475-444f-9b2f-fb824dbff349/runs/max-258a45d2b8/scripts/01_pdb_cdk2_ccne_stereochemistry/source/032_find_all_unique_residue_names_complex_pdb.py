
# Find all unique residue names in complex.pdb
resnames = set()
with open('complex.pdb') as f:
    for line in f:
        if line.startswith(('ATOM','HETATM')):
            resnames.add(line[17:20].strip())
print("All residue names in complex.pdb:", sorted(resnames))

# Check if UNL is still anywhere
with open('best_pose_lig.pdb') as f:
    content = f.read()
print("UNL in best_pose_lig.pdb:", 'UNL' in content)
print("LIG in best_pose_lig.pdb:", 'LIG' in content)
print("First HETATM line:", [l for l in content.split('\n') if 'HETATM' in l or 'ATOM' in l][:2])
