
from rdkit import Chem
import os

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
prot_sdf = os.path.join(wd, "all_protonated_3d.sdf")

suppl = Chem.SDMolSupplier(prot_sdf, removeHs=True, sanitize=True)
prot_info = {}
for m in suppl:
    if m:
        name = m.GetProp('_Name')
        prot_info[name] = Chem.GetFormalCharge(m)

# Top 10 + CTX-1017233 reference
top11 = [
    (1,  'CTX-1020521', 61),
    (2,  'CTX-1020520', 62),
    (3,  'CTX-1020810', 12),
    (4,  'CTX-1019660', 77),
    (5,  'CTX-1020458', 68),
    (6,  'CTX-1019813', 74),
    (7,  'CTX-1020882', 4),
    (8,  'CTX-1020555', 59),
    (9,  'CTX-1020816', 10),
    (10, 'CTX-1020751', 27),
    (13, 'CTX-1017233', 84),  # reference compound
]

print(f"{'Rank':>4}  {'Compound':30}  {'lig#':>5}  {'charge_pH74':>12}")
for rank, name, lig_n in top11:
    q = prot_info.get(name, '?')
    print(f"  {rank:2d}  {name:30}  lig{lig_n:<4}  q={q:+d}")
