
import math, json, os

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"

# Load scores
with open(os.path.join(wd, "docking_scores.json")) as f:
    results = json.load(f)

# ΔG → Ki → IC50 via Cheng-Prusoff
# Ki = exp(ΔG / RT); IC50 = Ki * (1 + [S]/Km) = 2*Ki (CDK2: [ATP]=10µM, Km=10µM)
R = 1.987e-3  # kcal/mol/K
T25 = 298.15
T37 = 310.15

def dg_to_ic50(dg, T=T25, factor=2.0):
    ki = math.exp(dg / (R * T)) * 1e9  # nM
    ic50 = ki * factor
    return ki, ic50

def fmt_nm(nm):
    if nm < 0.001: return f"{nm*1000:.1f} pM"
    if nm < 1:    return f"{nm*1000:.0f} pM"
    if nm < 1000: return f"{nm:.1f} nM"
    return f"{nm/1000:.2f} µM"

print(f"{'Rank':>4}  {'Compound':35}  {'Vina':>8}  {'Ki(25°C)':>12}  {'IC50(25°C)':>12}  {'Ki(37°C)':>12}  {'IC50(37°C)':>12}")
print("-"*108)

sorted_res = sorted(results, key=lambda x: x['best'] if x['best'] else 0)

for i, r in enumerate(sorted_res):
    if r['best'] is None: continue
    ki25, ic50_25 = dg_to_ic50(r['best'], T25)
    ki37, ic50_37 = dg_to_ic50(r['best'], T37)
    print(f"  {i+1:2d}  {r['name']:35}  {r['best']:>8.3f}  {fmt_nm(ki25):>12}  {fmt_nm(ic50_25):>12}  {fmt_nm(ki37):>12}  {fmt_nm(ic50_37):>12}")

# References
print("-"*108)
for label, dg in [("CTX crystal (score_only)", -14.090), ("CTX-1017233 exh=32 (prior)", -12.614)]:
    ki25, ic50_25 = dg_to_ic50(dg, T25)
    ki37, ic50_37 = dg_to_ic50(dg, T37)
    print(f"  --  {label:35}  {dg:>8.3f}  {fmt_nm(ki25):>12}  {fmt_nm(ic50_25):>12}  {fmt_nm(ki37):>12}  {fmt_nm(ic50_37):>12}")
