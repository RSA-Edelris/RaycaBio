
# Download PDB 4CI2 and inspect it
import urllib.request, os

pdb_path = 'PB-20260903-4CI2_raw.pdb'
url = 'https://files.rcsb.org/download/4CI2.pdb'
urllib.request.urlretrieve(url, pdb_path)
print(f"Downloaded: {pdb_path}  ({os.path.getsize(pdb_path):,} bytes)")

# Quick inspection
with open(pdb_path) as f:
    lines = f.readlines()

# Header / title
for line in lines[:10]:
    print(line.rstrip())

# Count chains, residues, SEQRES, missing residue hints
chains = set()
residues = set()
seqres = []
remark465 = []
hetnam = []
for line in lines:
    rec = line[:6].strip()
    if rec == 'ATOM':
        chains.add(line[21])
        residues.add((line[21], line[22:26].strip(), line[17:20].strip()))
    elif rec == 'SEQRES':
        seqres.append(line.rstrip())
    elif rec == 'REMARK' and '465' in line[:12]:
        remark465.append(line.rstrip())
    elif rec == 'HETNAM':
        hetnam.append(line.rstrip())

print(f"\nChains: {sorted(chains)}")
print(f"ATOM residues: {len(residues)}")
print(f"SEQRES lines: {len(seqres)}")
print(f"REMARK 465 (missing residues): {len(remark465)}")
print(f"HETNAM ligands: {hetnam[:10]}")

# Show first few SEQRES lines
print("\nFirst 4 SEQRES lines:")
for s in seqres[:4]:
    print(' ', s)

# Show REMARK 465 summary
print(f"\nFirst 6 REMARK 465 lines:")
for r in remark465[:6]:
    print(' ', r)
