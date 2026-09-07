
import sys, json
from collections import defaultdict
sys.path.insert(0, WORK)
from interaction_utils import summarise

# Load all contacts
with open(f"{WORK}/all_contacts.json") as f:
    all_contacts = json.load(f)

# ── interaction frequency table ───────────────────────────────────────────────
# For each (type, residue) pair, count how many of the 32 ligands form that contact
freq = defaultdict(lambda: defaultdict(int))
for name, contacts in all_contacts.items():
    s = summarise(contacts)
    for itype, res_list in s.items():
        for res in res_list:
            freq[itype][res] += 1

N = len(all_contacts)  # 32

# Sort by frequency descending within each type
print("INTERACTION FREQUENCY (n/32 ligands)\n")
for itype in ['H-bond', 'Hydrophobic', 'VdW']:
    if itype not in freq:
        continue
    sorted_res = sorted(freq[itype].items(), key=lambda x: -x[1])
    print(f"{'─'*42}")
    print(f"{itype}")
    print(f"{'─'*42}")
    for res, cnt in sorted_res[:15]:
        bar = '█' * cnt + '░' * (N - cnt)
        print(f"  {res:10s}  {cnt:3d}/{N}  {bar[:20]}")

# Save to JSON for report
freq_out = {itype: dict(sorted_res) for itype, sorted_res in freq.items()}
with open(f"{WORK}/interaction_freq.json", 'w') as f:
    json.dump(freq_out, f, indent=2)
