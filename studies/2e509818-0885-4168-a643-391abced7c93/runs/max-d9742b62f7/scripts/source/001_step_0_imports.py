
# ── Step 0: imports ──────────────────────────────────────────────────────────
import warnings, os
warnings.filterwarnings('ignore')
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors, Crippen
from rdkit.Chem import rdChemReactions

# ── Step 1: load amine ───────────────────────────────────────────────────────
amine_path = '/home/ubuntu/rayca-artifacts/8c1a5f76c0879e6c03b61ed2/files/amine.mol'
acid_path  = '/home/ubuntu/rayca-artifacts/8c1a5f76c0879e6c03b61ed2/files/acid.sdf'

amine = Chem.MolFromMolFile(amine_path, removeHs=False, sanitize=False)
Chem.SanitizeMol(amine)
amine = Chem.RemoveHs(amine)
print("Amine SMILES :", Chem.MolToSmiles(amine))
print("Amine atoms  :", amine.GetNumAtoms())

# Enumerate which NH groups exist
for a in amine.GetAtoms():
    if a.GetAtomicNum() == 7:
        print(f"  N idx={a.GetIdx()} totalHs={a.GetTotalNumHs()} "
              f"inRing={a.IsInRing()} arom={a.GetIsAromatic()} "
              f"degree={a.GetDegree()}")
