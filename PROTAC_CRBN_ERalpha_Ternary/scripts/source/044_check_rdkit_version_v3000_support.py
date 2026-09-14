
# Check RDKit version and V3000 support
from rdkit import Chem
print("RDKit version:", Chem.rdBase.rdkitVersion)

# Try reading a single V3000 molblock
test_block = """ARV-001
OCL MolfileCreator  2D

  0  0  0  0  0  0              0 V3000
M  V30 BEGIN CTAB
M  V30 COUNTS 4 4 0 0 0
M  V30 BEGIN ATOM
M  V30 1 C 0.0 0.0 0.0 0
M  V30 2 C 1.0 0.0 0.0 0
M  V30 3 C 1.0 1.0 0.0 0
M  V30 4 C 0.0 1.0 0.0 0
M  V30 END ATOM
M  V30 BEGIN BOND
M  V30 1 1 1 2
M  V30 2 1 2 3
M  V30 3 1 3 4
M  V30 4 1 4 1
M  V30 END BOND
M  V30 END CTAB
M  END
"""

mol = Chem.MolFromMolBlock(test_block)
print("Simple V3000 test:", mol)
if mol:
    print("SMILES:", Chem.MolToSmiles(mol))
