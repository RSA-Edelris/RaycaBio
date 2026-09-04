
# Step 1: Read SDF, inspect structure
from rdkit import Chem
from rdkit.Chem import PandasTools, SDMolSupplier
import pandas as pd

sdf_path = "/home/ubuntu/rayca-artifacts/11507a0e2f5e69d5dfa40a62/files/ASMS.sdf"

# Load into dataframe
df = PandasTools.LoadSDF(sdf_path, smilesName='SMILES', molColName='Mol', includeFingerprints=False)
print(f"Loaded: {len(df)} molecules")
print(f"Columns: {list(df.columns)}")
print(f"\nFirst few rows of relevant cols:")
# Find the activity column
for col in df.columns:
    if 'Hit' in col or 'hit' in col or 'class' in col.lower() or 'active' in col.lower() or 'P841' in col:
        print(f"  Activity col candidate: '{col}'")
        print(df[col].value_counts())
        print()
