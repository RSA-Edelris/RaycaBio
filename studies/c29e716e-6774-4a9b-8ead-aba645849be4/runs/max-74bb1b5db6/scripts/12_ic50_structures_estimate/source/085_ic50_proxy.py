
import numpy as np
from scipy import stats
import math

R = 0.001987; T = 310.0

# Calibration: use AS ratio as IC50 proxy with [P]=1 µM (typical ASMS)
# IC50_proxy(nM) = AS_ratio * 1000 nM  (Ki ≈ [P]*AS_ratio when AS_ratio<<1)
# This gives relative IC50s anchored to assumed [P]=1 µM

names_ka = [n for n, s, r in known_actives]
vina_ka  = np.array([docking_results[n] for n in names_ka])
as_ratio = np.array([r for n, s, r in known_actives])
ic50_proxy_nM = as_ratio * 1000.0  # nM, assuming [P]=1 µM

log_ic50 = np.log10(ic50_proxy_nM)
slope2, intercept2, r2, p2, se2 = stats.linregress(vina_ka, log_ic50)
print(f"Calibration: log10(IC50/nM) = {slope2:.4f}*ΔG + {intercept2:.4f}")
print(f"  R²={r2**2:.3f}  p={p2:.4f}")
print(f"  Vina RMSE ~1.5 kcal/mol → IC50 uncertainty factor ~{math.exp(1.5/(R*T)):.0f}×\n")

# Calibrated IC50 for all 35 compounds
def calibrated_ic50_nM(dG):
    log_ic50_pred = slope2 * dG + intercept2
    return 10**log_ic50_pred

def ic50_range(dG, delta=1.5):
    lo = 10**(slope2*(dG+delta)+intercept2)
    hi = 10**(slope2*(dG-delta)+intercept2)
    return lo, hi

proposed_names = [n for n, s in proposed]

print("=== PROPOSED COMPOUNDS — Calibrated IC50 ===")
print(f"{'Compound':<8} {'ΔG':>6} {'IC50 est':>12} {'IC50 range':>22} {'vs best known':>14}")
print("-"*68)
best_known_dG = min(docking_results[n] for n in names_ka)
for name in proposed_names:
    dG = docking_results[name]
    ic50 = calibrated_ic50_nM(dG)
    lo, hi = ic50_range(dG)
    delta_dG = dG - best_known_dG
    flag = " ★" if dG <= best_known_dG else ""
    print(f"{name:<8} {dG:>6.1f} {ic50:>10.0f}nM  [{lo:.0f}–{hi:.0f}] nM{flag}")

print()
print("=== KNOWN ACTIVES — Back-calculated ===")
print(f"{'Compound':<14} {'ΔG':>6} {'IC50(Vina)':>12} {'IC50(AS proxy)':>16}")
print("-"*52)
for name, smi, asr in known_actives:
    dG = docking_results[name]
    ic50v = calibrated_ic50_nM(dG)
    ic50a = asr*1000
    print(f"{name:<14} {dG:>6.1f} {ic50v:>10.0f}nM  {ic50a:>12.1f}nM")
