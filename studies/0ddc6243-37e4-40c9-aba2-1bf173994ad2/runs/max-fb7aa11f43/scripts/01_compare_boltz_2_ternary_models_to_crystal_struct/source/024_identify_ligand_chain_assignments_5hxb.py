
# Identify ligand and chain assignments in 5HXB
import gemmi, numpy as np

# Check non-polymer residues in chain Z (CRBN copy 1)
chain_Z = model['Z']
nonpoly = [r for r in chain_Z if r.entity_type == gemmi.EntityType.NonPolymer]
print("Chain Z non-polymer residues:")
for r in nonpoly:
    atoms = list(r)
    print(f"  {r.name} seqid={r.seqid} n_atoms={len(atoms)}")

chain_C = model['C']
nonpoly_C = [r for r in chain_C if r.entity_type == gemmi.EntityType.NonPolymer]
print("\nChain C non-polymer residues:")
for r in nonpoly_C:
    atoms = list(r)
    print(f"  {r.name} seqid={r.seqid} n_atoms={len(atoms)}")

# Get sequences for each chain to confirm identity
def get_sequence(chain):
    aa3to1 = gemmi.cif.read_string("""data_a""")  # won't work, use gemmi built-in
    seq = []
    for r in chain:
        if r.entity_type == gemmi.EntityType.Polymer:
            seq.append(r.name)
    return seq

# Use gemmi one-letter code
def chain_seq_1letter(chain):
    seq = []
    for r in chain:
        if r.entity_type == gemmi.EntityType.Polymer:
            try:
                seq.append(gemmi.find_tabulated_residue(r.name).one_letter_code)
            except:
                seq.append('X')
    return ''.join(seq)

for cname in ['X', 'Z', 'A', 'C']:
    s = chain_seq_1letter(model[cname])
    print(f"\nChain {cname} seq (len={len(s)}): {s[:30]}...{s[-10:]}")
