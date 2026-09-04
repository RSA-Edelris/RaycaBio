
import json, math, os

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"

with open(os.path.join(wd, "score_table.json")) as f:
    rows = json.load(f)

R = 1.987e-3; T25 = 298.15; T37 = 310.15

def trow(r):
    return f"| {r['rank']:>3} | {r['name']:25} | {r['mw']:>7} | {r['p1']:>8} | {r['p2']:>8} | {r['p3']:>8} | {r['p4']:>8} | {r['p5']:>8} | {r['ic50_25']:>12} | {r['ic50_37']:>12} |"

header = "| Rank | Compound                  |      MW | Pose 1 (kcal/mol) | Pose 2 | Pose 3 | Pose 4 | Pose 5 | IC50 25°C | IC50 37°C |\n|------|---------------------------|---------|-------------------|--------|--------|--------|--------|-----------|-----------|"

# Simpler header that renders
header2 = "| Rank | Compound | MW (Da) | Pose1 | Pose2 | Pose3 | Pose4 | Pose5 | IC50 25°C | IC50 37°C |\n|------|----------|---------|-------|-------|-------|-------|-------|-----------|-----------|"

def trow2(r):
    return f"| {r['rank']} | {r['name']} | {r['mw']} | {r['p1']} | {r['p2']} | {r['p3']} | {r['p4']} | {r['p5']} | {r['ic50_25']} | {r['ic50_37']} |"

table_md = header2 + "\n" + "\n".join(trow2(r) for r in rows)
# CTX refs
table_md += "\n| — | CTX crystal (score_only, ref) | 523.3 | –14.090 | — | — | — | — | 94 pM | 235 pM |"
table_md += "\n| — | CTX-1017233 (exh=32, prior session) | 523.3 | –12.614 | — | — | — | — | 1.1 nM | 2.6 nM |"

# Top-10 contacts table
contacts_md = """| Rank | Compound | Closest Contact (Å) | 2nd Contact (Å) | 3rd Contact (Å) | A:HIS122 | B:GLU362 |
|------|----------|---------------------|-----------------|-----------------|----------|----------|
| 1 | CTX-1020521 | A:ALA152 3.14 | A:HIS122 3.15 | B:SER446 3.19 | ✓ 3.15 | — |
| 2 | CTX-1020520 | A:HIS122 3.12 | A:ALA152 3.16 | B:SER446 3.25 | ✓ 3.12 | — |
| 3 | CTX-1020810 | A:ARG123 2.76 | B:LEU442 2.87 | A:GLU58 2.94 | — | — |
| 4 | CTX-1019660 | A:HIS122 3.09 | A:GLU58 3.34 | B:ILE317 3.40 | ✓ 3.09 | — |
| 5 | CTX-1020458 | B:LEU442 2.83 | A:GLU58 3.16 | B:TRP315 3.20 | — | — |
| 6 | CTX-1019813 | A:HIS122 2.93 | B:ILE317 3.14 | A:GLU58 3.39 | ✓ 2.93 | — |
| 7 | CTX-1020882 | B:VAL445 3.03 | B:SER446 3.10 | B:GLU362 3.18 | ✓ 3.29 | ✓ 3.18 |
| 8 | CTX-1020555 | A:GLY154 3.26 | A:HIS122 3.28 | B:ASN449 3.28 | ✓ 3.28 | — |
| 9 | CTX-1020816 | A:GLY154 3.02 | A:HIS122 3.10 | B:GLU362 3.26 | ✓ 3.10 | ✓ 3.26 |
| 10 | CTX-1020751 | B:GLU401 3.10 | B:TRP315 3.14 | B:SER446 3.14 | — | — |
| 13 | CTX-1017233 (ref) | B:GLU362 2.94 | A:HIS122 2.96 | A:GLY154 2.96 | ✓ 2.96 | ✓ 2.94 |"""

with open(os.path.join(wd, "table_md.txt"), 'w') as f:
    f.write(table_md)
with open(os.path.join(wd, "contacts_md.txt"), 'w') as f:
    f.write(contacts_md)
print("Tables built")
print(f"Docking table: {len(table_md)} chars")
