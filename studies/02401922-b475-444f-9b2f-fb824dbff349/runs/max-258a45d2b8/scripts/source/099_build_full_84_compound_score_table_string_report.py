
# Build the full 84-compound score table string for the report
import json, math, os

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"

with open(os.path.join(wd, "docking_scores.json")) as f:
    scores = json.load(f)
scores.sort(key=lambda x: x['best'] if x['best'] else 0)

R = 1.987e-3; T25 = 298.15; T37 = 310.15

def ic50(dg, T=T25, factor=2.0):
    ki = math.exp(dg / (R * T)) * 1e9
    return ki * factor

def fmt(v):
    if v < 1: return f"{v*1000:.0f} pM"
    if v < 1000: return f"{v:.1f} nM"
    return f"{v/1000:.2f} µM"

# Build table rows
rows = []
for i, r in enumerate(scores):
    if r['best'] is None: continue
    p = r['all_scores']
    ic = ic50(r['best'])
    def ps(j): return f"{p[j]:.3f}" if len(p)>j else "—"
    rows.append({
        'rank': i+1,
        'name': r['name'],
        'mw': r['mw'],
        'p1': ps(0), 'p2': ps(1), 'p3': ps(2), 'p4': ps(3), 'p5': ps(4),
        'ic50_25': fmt(ic),
        'ic50_37': fmt(ic50(r['best'], T37)),
    })

# Write scores table as JSON for report generation
with open(os.path.join(wd, "score_table.json"), 'w') as f:
    json.dump(rows, f, indent=2)

print(f"Score table saved: {len(rows)} rows")
print("Sample rows 1-5:")
for r in rows[:5]:
    print(f"  {r['rank']:2d}  {r['name']:25s}  {r['p1']:>8}  IC50(25°C)={r['ic50_25']}")
