
# Step 7: Decode scaffold and analyze R-groups
# Scaffold: bicyclic [pyridine+piperidine] with two amide arms
# Left arm: c(C(=O)NH-R2) on pyridine C5
# Right arm: piperidine-N-C(=O)-R1

# Let's convert the MCS SMARTS to a readable mol and get canonical SMILES
from rdkit.Chem import rdFMCS

# Re-run MCS, get canonical scaffold
active_mols_list = list(actives['std_mol'].dropna())
mcs = rdFMCS.FindMCS(active_mols_list, ringMatchesRingOnly=True, completeRingsOnly=True, timeout=30)
scaffold_mol = Chem.MolFromSmarts(mcs.smartsString)
print("MCS SMARTS (15-atom core):", mcs.smartsString)

# Map each active: what does R1 (piperidine N-acyl) and R2 (amide NH-R) look like?
print("\n--- R-group assignment from SMILES analysis ---")
print(f"{'EDS_Number':<15} {'Hit_rank':<10} {'AS ratio':<10} {'R1 (N-acyl on core)':<40} {'R2 (NH-arm)':<50}")
print("-"*130)

# Manual decomposition based on canonical SMILES patterns  
# Core: c1ccc2c(n1)CN(C(=O)...)CC2 + C(=O)NC...
import re

for _, row in actives.sort_values('Hit_rank').iterrows():
    smi = row['can_smiles']
    eds = row['EDS_Number']
    rank = row['Hit_rank']
    ras = row['AS ratio']
    
    # Extract R1: group after CN(C(=O) in piperidine N
    # Extract R2: group after C(=O)N in external arm
    # Simple: print SMILES fragment context
    # Find the bicyclic fragment
    core_patt = Chem.MolFromSmarts('O=C([NX3])c1ccc2c(n1)CN(C(=O))CC2')
    if not core_patt:
        core_patt = Chem.MolFromSmarts('[#6](=O)Nc1ccc2c(n1)CN(CC2)C(=O)')
    
    print(f"{eds:<15} {str(rank):<10} {str(ras):<10} {smi[:120]}")
