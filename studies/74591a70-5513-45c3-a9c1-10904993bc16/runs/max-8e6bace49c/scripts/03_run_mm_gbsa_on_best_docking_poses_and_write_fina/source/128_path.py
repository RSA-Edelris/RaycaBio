
import json
from pathlib import Path
BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")

# Load interaction fingerprints
fp_data = json.loads((BASE / "interaction_fingerprints.json").read_text())

# Show top interactions
print("=== TOP RESIDUE × INTERACTION FREQUENCY ===")
print(f"{'Residue':<22} {'Interaction':<18} {'Count':>6} {'Freq%':>7}")
print("─" * 56)

items = sorted(fp_data['residue_type_freq'].items(), key=lambda x: -x[1])
n = fp_data['n_compounds']
for key, count in items[:25]:
    res, itype = key.split('|')
    print(f"{res:<22} {itype:<18} {count:>6} {100*count/n:>6.0f}%")

print(f"\n=== INTERACTION TYPE TOTALS ===")
for itype, count in sorted(fp_data['interaction_type_counts'].items(), key=lambda x: -x[1]):
    print(f"  {itype:<18}: {count:>4} (across {n} compounds)")

# Also check per-compound summary
print(f"\n=== PER-COMPOUND INTERACTION COUNTS ===")
for name, ints in sorted(fp_data['fingerprints'].items()):
    n_int = len(ints) if isinstance(ints, list) else 0
    types = sorted(set(i['interaction'] for i in ints)) if isinstance(ints, list) else []
    print(f"  {name:<28} {n_int:>3} interactions: {', '.join(types[:5])}")
