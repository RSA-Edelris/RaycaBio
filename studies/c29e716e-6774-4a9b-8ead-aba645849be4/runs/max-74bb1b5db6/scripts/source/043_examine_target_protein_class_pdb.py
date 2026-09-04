
# Examine target protein class from PDB
pdb_path = "/home/ubuntu/rayca-artifacts/11507a0e2f5e69d5dfa40a62/files/Target.pdb"
with open(pdb_path) as f:
    lines = [l for l in f if l.startswith(('HEADER','TITLE','COMPND','KEYWDS','REMARK 2','SEQRES'))]
print(''.join(lines[:40]))
