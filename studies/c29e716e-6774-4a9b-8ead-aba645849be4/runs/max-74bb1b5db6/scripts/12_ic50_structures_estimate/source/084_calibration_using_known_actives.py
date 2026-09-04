
import numpy as np
from scipy import stats
import math

# --- Calibration using known actives ---
R = 0.001987  # kcal/mol/K
T = 310.0     # K

# Collect Vina scores and AS ratios
names_ka  = [n for n, s, r in known_actives]
vina_ka   = np.array([docking_results[n] for n in names_ka])
as_ratio  = np.array([r for n, s, r in known_actives])

# AS ratio: lower = tighter binder → log10(1/AS_ratio) = -log10(AS_ratio) is our "potency proxy"
neg_log_as = -np.log10(as_ratio)

# Linear regression: Vina_score vs -log10(AS_ratio)
slope, intercept, r_val, p_val, se = stats.linregress(vina_ka, neg_log_as)
print(f"Calibration: -log10(AS_ratio) = {slope:.4f}*Vina + {intercept:.4f}")
print(f"  R²={r_val**2:.3f}  p={p_val:.4f}  n=15")

# Known actives range for context
print(f"\nKnown actives Vina range: {vina_ka.min():.1f} to {vina_ka.max():.1f} kcal/mol")
print(f"AS ratio range: {as_ratio.min():.4f} to {as_ratio.max():.4f}")

# --- Thermodynamic IC50 from ΔG ---
def dG_to_IC50_nM(dG):
    Ki_M = math.exp(dG / (R * T))
    return Ki_M * 1e9  # nM

# Calibrated IC50: use empirical linear model anchored to known actives
# Strategy: find which known active has best-estimated IC50 from AS ratio
# AS ratio 0.03 is most potent known → use as anchor
# In ASMS, roughly: binding% = (1 - AS_ratio) 
# Ki estimate (rough): Ki ≈ [P] * AS_ratio/(1-AS_ratio) 
# We don't know [P] exactly, so use relative calibration

# Use Vina ΔG → Ki thermodynamic as primary; report ±1 kcal/mol uncertainty range
print("\n--- Thermodynamic IC50 for known actives ---")
for name, smi, asr in known_actives:
    dG = docking_results[name]
    ic50 = dG_to_IC50_nM(dG)
    print(f"  {name}: ΔG={dG:.1f}  IC50≈{ic50:.0f} nM  AS_ratio={asr:.3f}")
