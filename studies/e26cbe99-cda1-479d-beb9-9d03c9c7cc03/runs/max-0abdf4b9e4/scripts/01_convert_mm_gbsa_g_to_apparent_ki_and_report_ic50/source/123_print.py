
import math

RT = 0.5922  # kcal/mol at 298 K

results = [
    ("EDS01806218_ent2", -25.22, 5.82, "reliable"),
    ("EDS01889984",      -23.80, 2.64, "reliable"),
    ("EDS01806218_ent1", -20.75, 2.59, "reliable"),
    ("EDS01357518_ent1",  68.17, 57.57,"INVALID — topology defect"),
    ("EDS01357518_ent2",   None, None,  "pending — no trajectory yet"),
]

print(f"{'Compound':<22}  {'ΔG (kcal/mol)':>14}  {'SD':>6}  {'Ki_apparent':>14}  {'pKi':>5}  Notes")
print("-"*95)
for name, dg, sd, note in results:
    if dg is None:
        print(f"{name:<22}  {'—':>14}  {'—':>6}  {'—':>14}  {'—':>5}  {note}")
    elif "INVALID" in note:
        print(f"{name:<22}  {dg:>14.2f}  {sd:>6.2f}  {'INVALID':>14}  {'—':>5}  {note}")
    else:
        ki = math.exp(dg / RT)
        pki = -math.log10(ki)
        if ki < 1e-15:
            ki_str = f"{ki*1e18:.1f} aM"
        elif ki < 1e-12:
            ki_str = f"{ki*1e15:.1f} fM"
        elif ki < 1e-9:
            ki_str = f"{ki*1e12:.1f} pM"
        elif ki < 1e-6:
            ki_str = f"{ki*1e9:.1f} nM"
        else:
            ki_str = f"{ki*1e6:.1f} µM"
        print(f"{name:<22}  {dg:>14.2f}  {sd:>6.2f}  {ki_str:>14}  {pki:>5.1f}  {note}")

print()
print("=== RELATIVE RANKING (ΔΔG vs EDS01806218_ent2) ===")
ref = -25.22
print(f"{'Compound':<22}  {'ΔΔG (kcal/mol)':>16}  {'Fold vs ent2':>14}")
print("-"*58)
for name, dg, sd, note in results:
    if dg is not None and "INVALID" not in note:
        ddg = dg - ref
        fold = math.exp(-ddg / RT)
        print(f"{name:<22}  {ddg:>+16.2f}  {fold:>13.1f}x")
