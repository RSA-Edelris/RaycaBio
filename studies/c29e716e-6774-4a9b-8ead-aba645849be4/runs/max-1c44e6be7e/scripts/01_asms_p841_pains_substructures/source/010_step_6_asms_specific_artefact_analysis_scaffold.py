
# Step 6: ASMS-specific artefact analysis + scaffold decomposition
from rdkit.Chem import rdFMCS, AllChem
import numpy as np

# ASMS-specific: check AS ratio distribution vs inactives
# AS ratio: higher = more compound retained with protein = more likely binder
# In ASMS typical noise level: AS ratio ~ 0 for inactives
# Aggregators show very HIGH AS ratio due to non-specific sequestration

active_as = actives['AS ratio'].astype(float)
inactive_as = df[df['HIT P841']=='Inactive']['AS ratio'].astype(float)
print(f"Active AS ratio: min={active_as.min():.4f}, max={active_as.max():.4f}, mean={active_as.mean():.4f}")
print(f"Inactive AS ratio: min={inactive_as.min():.6f}, max={inactive_as.max():.4f}, mean={inactive_as.mean():.6f}")

# ASMS dimer artefact: compound that appears as dimer?
# Check if any active MW ≈ 2x another compound's MW (±2 Da)
print("\n--- Dimer check: any active MW ≈ 2x any compound? ---")
all_mws = df['MW'].dropna().values
for _, row in actives.iterrows():
    half_mw = row['MW'] / 2.0
    close = np.abs(all_mws - half_mw) < 2.0
    if close.sum() > 0:
        print(f"  {row['EDS_Number']} MW={row['MW']:.1f}: {close.sum()} compounds at MW≈{half_mw:.1f}")

# Retention time analysis for MS artefacts
print("\n--- RT analysis ---")
print(f"Active RT range: {actives['RTmin'].astype(float).min():.2f} - {actives['RTmin'].astype(float).max():.2f} min")
print(f"Inactive RT range: {inactive_as.index}... (checking distribution)")
inactive_rt = df[df['HIT P841']=='Inactive']['RTmin'].astype(float)
print(f"Inactive RT: mean={inactive_rt.mean():.2f}, std={inactive_rt.std():.2f}")
print(f"Early eluters (<0.8 min) in actives: {(actives['RTmin'].astype(float)<0.8).sum()}")

# Scaffold analysis using MCS
print("\n--- MCS scaffold across all 15 actives ---")
active_mols = [m for m in actives['std_mol'] if m is not None]
mcs_result = rdFMCS.FindMCS(active_mols, 
                             ringMatchesRingOnly=True,
                             completeRingsOnly=True,
                             timeout=30)
print(f"MCS SMARTS: {mcs_result.smartsString}")
print(f"MCS atoms: {mcs_result.numAtoms}, bonds: {mcs_result.numBonds}")
