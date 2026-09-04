
import math

R = 0.001987   # kcal / (mol·K)
T25 = 298.15   # 25 C
T37 = 310.15   # 37 C

def dg_to_ki(dg, T):
    return math.exp(dg / (R * T))

def fmt(v):
    if v < 1e-9:  return f"{v*1e12:.1f} pM"
    if v < 1e-6:  return f"{v*1e9:.2f} nM"
    if v < 1e-3:  return f"{v*1e6:.2f} µM"
    return f"{v*1e3:.1f} mM"

# Cheng-Prusoff: IC50 = Ki * (1 + [S]/Km)
# CDK2 assay: [ATP]=10 µM, Km(ATP)=10 µM (typical) → factor = 2
CP = 2.0

vina = [
    ("Pose 1 (best)",  -12.614),
    ("Pose 2",         -12.195),
    ("Pose 3",         -11.141),
    ("Pose 4",         -10.657),
    ("Pose 5",         -10.389),
    ("CTX crystal",    -14.086),
]

hdr = f"{'Source':<18} {'ΔG':>7} {'Ki 25°C':>10} {'IC50 25°C':>11} {'Ki 37°C':>10} {'IC50 37°C':>11}"
print(hdr)
print("-"*72)
for name, dg in vina:
    ki25  = dg_to_ki(dg, T25)
    ki37  = dg_to_ki(dg, T37)
    print(f"{name:<18} {dg:>7.3f} {fmt(ki25):>10} {fmt(ki25*CP):>11} {fmt(ki37):>10} {fmt(ki37*CP):>11}")

print()
print("MD-averaged MM/GBSA expected range:")
for dg in [-20, -30, -40, -50]:
    ki = dg_to_ki(dg, T25)
    print(f"  ΔG={dg:4d} → Ki={fmt(ki)}, IC50={fmt(ki*CP)}")

print()
print("Notes:")
print("  Cheng-Prusoff: [ATP]=10 µM, Km(ATP,CDK2)=10 µM → IC50=2·Ki")
print("  Vina ±1-2 kcal/mol → IC50 uncertainty ~5-50x")
print("  MM/GBSA single-frame (+9.67 / −76.69 kcal/mol): not converted (unphysical bracket)")
