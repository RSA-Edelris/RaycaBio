
# ── Interaction frequency statistics across all 5 poses ─────────────────────
from collections import defaultdict

hbond_freq  = defaultdict(int)
hphob_freq  = defaultdict(int)

for r in interaction_results:
    for hb in r["hbonds"]:
        key = f"{hb[0]}{hb[1]} ({hb[2]})"
        hbond_freq[key] += 1
    for hp in r["hydrophobic"]:
        key = f"{hp[0]}{hp[1]}"
        hphob_freq[key] += 1

print("H-bond frequency across 5 poses:")
for k, v in sorted(hbond_freq.items(), key=lambda x: -x[1]):
    bar = "█" * v
    print(f"  {k:<25} {v}/5  {bar}")

print("\nHydrophobic contact frequency:")
for k, v in sorted(hphob_freq.items(), key=lambda x: -x[1]):
    bar = "█" * v
    print(f"  {k:<15} {v}/5  {bar}")
