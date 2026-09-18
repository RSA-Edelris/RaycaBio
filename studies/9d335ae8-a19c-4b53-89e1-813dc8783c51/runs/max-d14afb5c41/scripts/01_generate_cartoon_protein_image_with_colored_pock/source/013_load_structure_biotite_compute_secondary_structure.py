
# Load structure with biotite and compute secondary structure
import biotite.structure as struc
import biotite.structure.io.pdb as pdb

pdb_file = pdb.PDBFile.read("/home/ubuntu/rayca-artifacts/c2db8d53fb710fe21c5fee43/files/CRBN.pdb")
structure = pdb.get_structure(pdb_file, model=1)
print(f"Atoms: {len(structure)}, Chains: {set(structure.chain_id)}")
print(f"Res range: {structure.res_id.min()} – {structure.res_id.max()}")

# Get protein-only atoms
protein_mask = struc.filter_amino_acids(structure)
protein = structure[protein_mask]
print(f"Protein atoms: {len(protein)}")

# Compute secondary structure with biotite (no DSSP needed)
# biotite has struc.annotate_sse which uses P-SEA algorithm
sse = struc.annotate_sse(protein)
print(f"\nSSE array length: {len(sse)}")
print(f"SSE unique values: {set(sse)}")
print("First 40:", sse[:40])
