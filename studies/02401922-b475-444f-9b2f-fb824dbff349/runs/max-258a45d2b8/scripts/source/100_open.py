
import json, math, os

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"

with open(os.path.join(wd, "score_table.json")) as f:
    rows = json.load(f)

R = 1.987e-3; T25 = 298.15; T37 = 310.15
def ic50(dg, T, factor=2.0):
    return math.exp(dg / (R*T)) * 1e9 * factor
def fmt(v):
    if v < 1: return f"{v*1000:.0f} pM"
    if v < 1000: return f"{v:.1f} nM"
    return f"{v/1000:.2f} µM"

# Build markdown docking table (split: top 30 detail, rest compact)
def trow(r):
    return f"| {r['rank']:>3} | {r['name']:25} | {r['mw']:>7} | {r['p1']:>8} | {r['p2']:>8} | {r['p3']:>8} | {r['p4']:>8} | {r['p5']:>8} | {r['ic50_25']:>12} | {r['ic50_37']:>12} |"

header = "| Rank | Compound                  |      MW | Pose 1   | Pose 2   | Pose 3   | Pose 4   | Pose 5   |  IC50 25°C |  IC50 37°C |\n|------|---------------------------|---------|----------|----------|----------|----------|----------|------------|------------|"

table_all = header + "\n" + "\n".join(trow(r) for r in rows)

# Store for use in report
print(f"Table rows: {len(rows)}")
print(table_all[:600])
