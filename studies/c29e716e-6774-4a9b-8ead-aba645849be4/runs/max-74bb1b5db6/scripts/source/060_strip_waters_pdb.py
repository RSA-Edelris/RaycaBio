
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter
import io, os

# Strip waters from PDB
lines_protein = [l for l in pdb_content.split('\n') if not (l.startswith('HETATM') and 'HOH' in l)]
pdb_clean = '\n'.join(lines_protein)
print(f"Original PDB: {len(pdb_content)} bytes, cleaned: {len(pdb_clean)} bytes")

# Write cleaned PDB to disk
pdb_clean_path = '/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02/target_clean.pdb'
with open(pdb_clean_path, 'w') as f:
    f.write(pdb_clean)

# Prepare EDS00444974 (simplest, cleanest active) as SDF for gnina
smi_anchor = 'Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)C(C)C)CC3)cn1'
mol = Chem.MolFromSmiles(smi_anchor)
mol = Chem.AddHs(mol)
AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
AllChem.MMFFOptimizeMolecule(mol)

sdf_path_anchor = '/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02/anchor.sdf'
with Chem.SDWriter(sdf_path_anchor) as w:
    w.write(mol)
print(f"Anchor SDF written: {sdf_path_anchor}")
print(f"Cleaned PDB: {len(pdb_clean)} bytes ({len(pdb_clean)//1024} KB)")
