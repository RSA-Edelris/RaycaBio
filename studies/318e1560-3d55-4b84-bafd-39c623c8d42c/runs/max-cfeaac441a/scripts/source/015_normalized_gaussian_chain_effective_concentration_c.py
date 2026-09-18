
# ── Normalized Gaussian-chain effective concentration ──
# C_eff = (3/(2πnb²))^(3/2) × exp(-3d²/(2nb²)) × 4πd² × (1Å³/1L conversion)
# Units: molecules/Å³ → multiply by (1e27/6.022e23) to get mol/L
# Optimal n for maximum Ceff at distance d: n* = d²/b²

from scipy.constants import Avogadro

b = 1.5   # Å per bond
AA3_PER_LITRE = 1e27  # Å³ per litre

def ceff_molar(d, n, b=1.5):
    """Effective concentration (mol/L) from Gaussian chain model."""
    if n <= 0: return 0.0
    sigma2 = n * b**2 / 3.0         # variance of each component
    prefac = (1/(2*np.pi*sigma2))**1.5  # (Å^-3)
    gauss  = np.exp(-d**2 / (2*sigma2))
    prob_density = prefac * gauss     # radial probability density at r=d (Å^-3·Å^-2 * 4πd²)
    # Full P(r=d) per unit d: 4πd² × prefac × gauss  [Å^-3]
    Pd = 4*np.pi*d**2 * prefac * gauss   # Å^-3
    return Pd * AA3_PER_LITRE / Avogadro  # mol/L

# Required distance for BD1→VHL
d_bd1 = bd1_exit_to_vhl_exit   # 5.6 Å
d_bd2 = mz1_bridge              # 5.0 Å (MZ1 crystal reference)
n_opt = (d_bd1 / b)**2
print(f"Required bridging distance (BD1): {d_bd1:.1f} Å  |  BD2 crystal ref: {d_bd2:.1f} Å")
print(f"Optimal chain length n* = d²/b² = {n_opt:.1f} heavy atoms\n")

linkers = [
    ("L1-short",   4,  "~4-atom alkyl/ether"),
    ("L2-medium",  8,  "PEG2-amide, 8 atoms"),
    ("L3-long",    12, "PEG3/PEG4 (~MZ1 length)"),
    ("L4-xlong",   18, "PEG5-PEG6, extra long"),
]

print(f"{'Linker':<14} {'n_atoms':>7} {'max_ext(Å)':>10} {'Ceff_BD1(mM)':>13} "
      f"{'Ceff_BD2(mM)':>13} {'strain_ratio':>12} {'rank_BD1':>9}")
print("-"*80)

ceff_bd1 = {}
for label, n_atoms, desc in linkers:
    ce1 = ceff_molar(d_bd1, n_atoms) * 1000   # mM
    ce2 = ceff_molar(d_bd2, n_atoms) * 1000   # mM
    max_ext = n_atoms * b
    strain  = d_bd1 / max_ext   # 1.0 = fully extended, ideal << 1
    ceff_bd1[label] = ce1
    print(f"{label:<14} {n_atoms:>7} {max_ext:>10.1f} {ce1:>13.3f} {ce2:>13.3f} "
          f"{strain:>12.3f}")

# Rank by Ceff at BD1 geometry
ranked = sorted(ceff_bd1.items(), key=lambda x: -x[1])
print(f"\nRanking by C_eff (highest = most cooperative):")
for rank, (label, ce) in enumerate(ranked, 1):
    print(f"  #{rank}: {label}  C_eff = {ce:.3f} mM")

print(f"\nCalibration: MZ1 (n≈12 atoms, d_BD2={d_bd2:.1f}Å) → "
      f"C_eff = {ceff_molar(d_bd2,12)*1000:.3f} mM")
print(f"  MZ1 cooperativity α=~31 (Gadd 2017); C_eff should be ~10-100 mM for productive PROTACs")
