
from rdkit import Chem
from rdkit.Chem import AllChem
import os

# ----------------------------------------------------------------
# Write all compounds to SDF with ETKDG 3D coords
# Includes: 15 actives + 38 designed analogues
# ----------------------------------------------------------------

all_cpds = []

# --- Actives ---
for a in actives_sorted:
    m = Chem.MolFromSmiles(a['smiles'])
    if m:
        m = Chem.AddHs(m)
        params = AllChem.ETKDGv3()
        params.randomSeed = 42
        r = AllChem.EmbedMolecule(m, params)
        if r == 0:
            AllChem.MMFFOptimizeMolecule(m)
            m.SetProp('_Name', a['name'])
            m.SetProp('AS_ratio', str(a['as1']))
            m.SetProp('type', 'active')
            all_cpds.append(m)
        else:
            print(f"  Embed failed for active {a['name']}")

# --- Designed analogues ---
for d in valid:
    m = Chem.MolFromSmiles(d['smiles'])
    if m:
        m = Chem.AddHs(m)
        params = AllChem.ETKDGv3()
        params.randomSeed = 42
        r = AllChem.EmbedMolecule(m, params)
        if r == 0:
            AllChem.MMFFOptimizeMolecule(m)
            m.SetProp('_Name', d['code'])
            m.SetProp('type', 'designed')
            all_cpds.append(m)
        else:
            print(f"  Embed failed for designed {d['code']}")

print(f"Total compounds with 3D coords: {len(all_cpds)}")

# Write to SDF
writer = Chem.SDWriter('/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d/ligands_3d.sdf')
for m in all_cpds:
    writer.write(m)
writer.close()
print("Written: ligands_3d.sdf")

# ----------------------------------------------------------------
# Prepare receptor: strip HETATM (CTX, waters), keep ATOM records
# ----------------------------------------------------------------
rec_lines = []
with open(PDB_PATH) as f:
    for line in f:
        if line.startswith('ATOM') or line.startswith('TER') or line.startswith('END'):
            rec_lines.append(line)

rec_path = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d/receptor_stripped.pdb'
with open(rec_path, 'w') as f:
    f.writelines(rec_lines)
print(f"Receptor written: {len(rec_lines)} lines")

# Print box parameters
print(f"\nDocking box centre: [{ctx_centroid[0]:.2f}, {ctx_centroid[1]:.2f}, {ctx_centroid[2]:.2f}]")
bbox_size = ctx_max - ctx_min
padded = bbox_size + 8   # 4 Å padding each side
print(f"CTX bbox size: {bbox_size.round(1)}")
print(f"Docking box (padded 8 Å): {padded.round(1)}")
