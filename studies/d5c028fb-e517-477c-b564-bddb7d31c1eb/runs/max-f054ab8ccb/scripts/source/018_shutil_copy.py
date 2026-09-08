
import shutil, os

wd = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d'

# Save actives docked output before next batch overwrites it
shutil.copy(f'{wd}/gnina_docked.sdf.gz', f'{wd}/actives_docked.sdf.gz')
print("Saved actives_docked.sdf.gz")

# Quick parse to check how many compounds were docked
import gzip
from rdkit import Chem

gz_path = f'{wd}/actives_docked.sdf.gz'
with gzip.open(gz_path, 'rt') as fh:
    content = fh.read()

# Count molecule records
mol_count = content.count('$$$$')
print(f"Poses in actives_docked.sdf.gz: {mol_count}")
# Show first 60 chars of properties for first few mols
lines = content.split('\n')
name_lines = [l.strip() for l in lines if l.strip() and not l.startswith('  ') and not l.startswith('V') and not l.startswith('M') and not l.startswith('>')]
print('\n'.join(name_lines[:20]))
