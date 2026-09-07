
import urllib.request, os

# Fetch 1Z5M from RCSB
url = "https://files.rcsb.org/download/1Z5M.pdb"
out = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/1Z5M.pdb"
urllib.request.urlretrieve(url, out)
size = os.path.getsize(out)
print(f"Downloaded 1Z5M.pdb: {size} bytes")

# Quick inspection - chains, residues, ligands, missing residues
lines = open(out).readlines()
chains = set()
hetatms = {}
seqres_res = {}
atom_residues = {}

for l in lines:
    if l.startswith("ATOM"):
        ch = l[21]
        rname = l[17:20].strip()
        rnum = int(l[22:26].strip())
        chains.add(ch)
        atom_residues.setdefault(ch, set()).add((rnum, rname))
    elif l.startswith("HETATM"):
        rname = l[17:20].strip()
        ch = l[21]
        rnum = int(l[22:26].strip())
        if rname not in ("HOH","WAT"):
            hetatms.setdefault(rname, []).append((ch, rnum))
    elif l.startswith("SEQRES"):
        ch = l[11]
        seqres_res.setdefault(ch, []).extend(l[19:].split())
    elif l.startswith("REMARK 465"):
        pass  # missing residues

print(f"Chains: {sorted(chains)}")
print(f"Ligands (non-water HETATM): {list(hetatms.keys())}")
for lig, positions in hetatms.items():
    print(f"  {lig}: {positions[:5]}")

# Count waters
waters = sum(1 for l in lines if l.startswith("HETATM") and l[17:20].strip() in ("HOH","WAT"))
print(f"Crystallographic waters: {waters}")
