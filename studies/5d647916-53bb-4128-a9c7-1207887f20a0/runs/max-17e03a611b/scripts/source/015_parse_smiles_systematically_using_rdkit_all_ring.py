
# Parse SMILES systematically using RDKit for all ring systems mentioned in the audit

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem
    print("RDKit available")
except ImportError:
    print("RDKit not available")
