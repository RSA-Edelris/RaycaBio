
pdb_path = "/home/ubuntu/rayca-artifacts/5e3a2eab5918b528d391eb88/files/CDK2-CCNE.pdb"

atoms = []
hetatm = []
with open(pdb_path) as fh:
    for line in fh:
        rec = line[:6].strip()
        if rec in ("ATOM", "HETATM"):
            try:
                name   = line[12:16].strip()
                resn   = line[17:20].strip()
                chain  = line[21]
                resseq = int(line[22:26])
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                entry = dict(rec=rec, name=name, resn=resn, chain=chain,
                             resseq=resseq, x=x, y=y, z=z)
                atoms.append(entry)
                if rec == "HETATM":
                    hetatm.append(entry)
            except Exception:
                pass

from collections import defaultdict
chains = defaultdict(set)
for a in atoms:
    if a['rec'] == 'ATOM':
        chains[a['chain']].add(a['resseq'])

print("ATOM chains:")
for c, rs in sorted(chains.items()):
    print(f"  Chain {c}: residues {min(rs)}-{max(rs)}  ({len(rs)} residues)")

het_ids = defaultdict(set)
for a in hetatm:
    het_ids[a['resn']].add(a['chain'])
print("\nHETATM residues:", dict(het_ids))
