
import urllib.request, os, gemmi

pdb_path = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/5HXB.cif"
if not os.path.exists(pdb_path):
    urllib.request.urlretrieve("https://files.rcsb.org/download/5HXB.cif", pdb_path)
print(f"File: {os.path.getsize(pdb_path):,} bytes")

# Inspect 5HXB chain contents
st = gemmi.read_structure(pdb_path)
model = st[0]
for chain in model:
    residues = list(chain)
    types = set(r.entity_type for r in residues)
    # Sample residue names
    sample = [r.name for r in residues[:5]]
    n_res = len(residues)
    n_atoms = sum(len(list(r)) for r in residues)
    print(f"Chain {chain.name}: {n_res} residues, {n_atoms} atoms | sample: {sample} | entity_types: {types}")
