
# Deeper inspection of 5T35: identify which chains are VHL, ElonginC/B, BRD4-BD2, and the PROTAC
# Chain lengths and residue ranges will identify the roles

def parse_pdb_summary(path):
    from collections import defaultdict
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

def chain_residue_count(path, chain_id):
    seen = set()
    with open(path) as f:
        for line in f:
            if line[:4] == "ATOM" and line[21] == chain_id:
                resnum = int(line[22:26])
                seen.add(resnum)
    return len(seen)

def chain_residue_range(path, chain_id):
    resnums = []
    seen_res = set()
    seq = []
    aa3 = {}
    with open(path) as f:
        for line in f:
            if line[:4] == "ATOM" and line[21] == chain_id and line[12:16].strip() == "CA":
                resnum = int(line[22:26])
                resname = line[17:20].strip()
                if resnum not in seen_res:
                    resnums.append(resnum)
                    seen_res.add(resnum)
                    seq.append(resname)
    return resnums[0] if resnums else None, resnums[-1] if resnums else None, len(resnums)

pdb5 = work_dir / "5T35.pdb"
print("5T35 chain summary:")
for ch in "ABCDEFGH":
    r0, r1, n = chain_residue_range(pdb5, ch)
    print(f"  chain {ch}: {n} residues, {r0}–{r1}")

# Also extract SEQRES to get protein identity
print("\nSEQRES records (first 3 per chain):")
seqres = {}
with open(pdb5) as f:
    for line in f:
        if line[:6] == "SEQRES":
            ch = line[11]
            residues = line[19:].split()
            seqres.setdefault(ch, []).extend(residues)
for ch, res in sorted(seqres.items()):
    print(f"  chain {ch} ({len(res)} aa): {res[:5]}...{res[-3:]}")
