
# ── Composite cooperativity model (calibrated) ──
# P_vec(r=d) = (1/(2π σ²))^(3/2) × exp(-d²/(2σ²))  [Å^-3] — probability per unit volume
# Ceff_raw  = P_vec × (Å³/L) / N_A
# Calibrate to MZ1: n=12, d_BD2=5.0 Å, measured α_BD2 = 31 (Gadd et al. 2017)
# Then α_BD1_Lx = 31 × [P_vec(Lx, d_BD1) / P_vec(12, d_BD2)] × [pose_fraction(Lx) / pose_fraction_MZ1]

from scipy.constants import Avogadro
AA3_PER_L = 1e27

d_bd1   = bd1_exit_to_vhl_exit   # 5.6 Å
d_bd2   = mz1_bridge              # 5.0 Å (MZ1 reference)
b       = 1.5
alpha_mz1 = 31.0   # Gadd 2017

def p_vec(d, n, b=1.5):
    """Probability density per unit volume at distance d (Å^-3)."""
    sigma2 = n * b**2 / 3.0
    return (1/(2*np.pi*sigma2))**1.5 * np.exp(-d**2 / (2*sigma2))

# MZ1 calibration reference
p_mz1  = p_vec(d_bd2, 12)
ceff_mz1_mM = p_mz1 * AA3_PER_L / Avogadro * 1000

linkers = [
    ("L1-short",   4,  4,  "4-atom alkyl/ether"),
    ("L2-medium",  8,  8,  "PEG2-amide, 8 atoms"),
    ("L3-long",   12, 12,  "PEG3/PEG4 (~MZ1)"),
    ("L4-xlong",  18, 16,  "PEG5-PEG6, extra long"),
]

# Pose acceptance fractions from ensemble (computed above)
pose_frac = {"L1-short": 2095/5000, "L2-medium": 4962/5000,
             "L3-long": 4981/5000,  "L4-xlong": 4980/5000}
pose_frac_mz1 = 4981/5000   # MZ1-like (n=12) reference

n_opt = (d_bd1/b)**2
print(f"Gaussian-chain optimal n* = {n_opt:.1f} heavy atoms  (for d={d_bd1:.1f} Å, b={b} Å)")
print(f"MZ1 calibration: n=12, d={d_bd2:.1f} Å, α_BD2={alpha_mz1}, "
      f"Ceff_raw = {ceff_mz1_mM:.1f} mM (Gaussian overestimate)\n")

print(f"{'Linker':<14} {'n':>4} {'max(Å)':>8} {'P_vec_ratio':>12} "
      f"{'pose_frac':>10} {'α_pred_BD1':>12} {'rank':>5}")
print("-"*65)

alpha_preds = {}
for label, n_real, n_eff, desc in linkers:
    pv    = p_vec(d_bd1, n_real)
    ratio = pv / p_mz1                      # relative Ceff vs MZ1 reference
    pf    = pose_frac[label]
    alpha = alpha_mz1 * ratio * (pf / pose_frac_mz1)  # scaled alpha
    alpha_preds[label] = alpha
    max_e = n_real * b
    print(f"{label:<14} {n_real:>4} {max_e:>8.1f} {ratio:>12.4f} {pf:>10.4f} {alpha:>12.2f}")

ranked = sorted(alpha_preds.items(), key=lambda x: -x[1])
print(f"\nFinal ranking by predicted α (BD1-targeting PROTAC):")
for rank, (label, alpha) in enumerate(ranked, 1):
    stars = "★" * (4 - rank + 1)
    delta = alpha - alpha_preds[ranked[0][0]] if rank > 1 else 0.0
    note  = "" if rank == 1 else f"  (−{abs(delta):.1f} vs #1)"
    print(f"  #{rank} {stars}  {label:<14}  α_pred ≈ {alpha:.1f}{note}")

print(f"\n  Note: α_pred is relative to MZ1/BD2 (α=31). "
      f"BD1-VHL intrinsic PPI ΔG is unknown — "
      f"absolute values carry BD1-VHL interface uncertainty (see falsification).")
