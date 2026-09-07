
import subprocess, os

# Write a standalone parmed conversion script
pmd_script = f'''\
import parmed as pmd
import sys

amber_sys = pmd.load_file("{MD_DIR}/complex.prmtop", "{MD_DIR}/complex.inpcrd")
n = len(amber_sys.atoms)
r = len(amber_sys.residues)
b = amber_sys.box
print(f"atoms={{n}} residues={{r}} box={{b[0]:.2f}}x{{b[1]:.2f}}x{{b[2]:.2f}}")

amber_sys.save("{MD_DIR}/complex.top", overwrite=True)
amber_sys.save("{MD_DIR}/complex.gro", overwrite=True)
print("DONE")
'''

pmd_script_path = f'{MD_DIR}/run_parmed.py'
with open(pmd_script_path, 'w') as fh:
    fh.write(pmd_script)

# Run with the conda python that has parmed
python = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/python3'
r = subprocess.run([python, pmd_script_path],
                   capture_output=True, text=True, cwd=MD_DIR)
print("stdout:", r.stdout)
if r.stderr:
    print("stderr:", r.stderr[-500:])

for fname in ['complex.top', 'complex.gro']:
    path = f'{MD_DIR}/{fname}'
    if os.path.exists(path):
        print(f"  {fname}: {os.path.getsize(path):,} bytes")
    else:
        print(f"  {fname}: MISSING")
