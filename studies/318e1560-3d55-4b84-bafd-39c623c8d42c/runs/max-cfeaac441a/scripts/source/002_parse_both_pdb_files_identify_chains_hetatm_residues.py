
# Parse both PDB files: identify chains, HETATM residues, resolution
from collections import defaultdict

def parse_pdb_summary(path):
    chains = defaultdict(set)
    hetatm = defaultdict(set)
    remarks = []
    with open(path) as f:
        for line in f:
            rt = line[:6].strip()
            if rt == "ATOM":
                chain = line[21]
                resname = line[17:20].strip()
                chains[chain].add(resname)
            elif rt == "HETATM":
                chain = line[21]
                resname = line[17:20].strip()
                hetatm[chain].add(resname)
            elif rt in ("REMARK", "TITLE", "EXPDTA"):
                remarks.append(line.rstrip())
    return chains, hetatm, [r for r in remarks if any(k in r for k in ("RESOLUTION", "TITLE", "EXPDTA"))]

for pdb_id in ["3MXF", "5T35"]:
    path = work_dir / f"{pdb_id}.pdb"
    chains, hetatm, remarks = parse_pdb_summary(path)
    print(f"\n=== {pdb_id} ===")
    for r in remarks[:6]:
        print(" ", r)
    print("  Protein chains:", {k: sorted(v)[:3] for k, v in chains.items()})
    print("  HETATM chains:", {k: sorted(v) for k, v in hetatm.items()})
