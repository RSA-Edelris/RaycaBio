
from rdkit.Chem import rdFMCS
import numpy as np

# Fix: convert with pd.to_numeric
active_as = pd.to_numeric(actives['AS ratio'], errors='coerce')
inactive_as = pd.to_numeric(df[df['HIT P841']=='Inactive']['AS ratio'], errors='coerce')
print(f"Active AS ratio: min={active_as.min():.4f}, max={active_as.max():.4f}, mean={active_as.mean():.4f}")
print(f"Inactive AS ratio: min={inactive_as.min():.6f}, max={inactive_as.max():.4f}, mean={inactive_as.mean():.6f}")

# Dimer artefact check
all_mws = pd.to_numeric(df['MW'], errors='coerce').dropna().values
print("\n--- Dimer check (active MW ≈ 2x any compound) ---")
for _, row in actives.iterrows():
    half_mw = row['MW'] / 2.0
    close = np.sum(np.abs(all_mws - half_mw) < 2.0)
    if close > 0:
        print(f"  {row['EDS_Number']} MW={row['MW']:.1f}: {close} compounds at ~{half_mw:.1f} Da")

# RT analysis
active_rt = pd.to_numeric(actives['RTmin'], errors='coerce')
inactive_rt = pd.to_numeric(df[df['HIT P841']=='Inactive']['RTmin'], errors='coerce')
print(f"\nActive RT: {active_rt.min():.2f}–{active_rt.max():.2f} min (mean {active_rt.mean():.2f})")
print(f"Inactive RT: mean={inactive_rt.mean():.2f}, std={inactive_rt.std():.2f}")

# MCS scaffold across all 15 actives
active_mols = [m for m in actives['std_mol'] if m is not None]
mcs = rdFMCS.FindMCS(active_mols, ringMatchesRingOnly=True, completeRingsOnly=True, timeout=30)
print(f"\n--- MCS (all 15 actives) ---")
print(f"SMARTS: {mcs.smartsString}")
print(f"Size: {mcs.numAtoms} atoms, {mcs.numBonds} bonds")

# MCS on top-ranked clean actives (exclude PAINS, just to see core)
clean_idx = actives[~actives['has_PAINS']].index
clean_mols = [actives.loc[i,'std_mol'] for i in clean_idx if actives.loc[i,'std_mol']]
mcs2 = rdFMCS.FindMCS(clean_mols, ringMatchesRingOnly=True, completeRingsOnly=True, timeout=30)
print(f"\n--- MCS (12 non-PAINS actives) ---")
print(f"SMARTS: {mcs2.smartsString}")
print(f"Size: {mcs2.numAtoms} atoms, {mcs2.numBonds} bonds")
