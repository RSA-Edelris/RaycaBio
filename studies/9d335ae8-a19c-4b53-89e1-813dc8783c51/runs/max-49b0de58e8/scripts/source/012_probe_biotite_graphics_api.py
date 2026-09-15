
# Probe biotite graphics API
import biotite
import biotite.structure as struc
import biotite.structure.io.pdb as pdb
import biotite.graphics as graphics
import inspect

# What's in biotite.graphics?
members = [m for m in dir(graphics) if not m.startswith('_')]
print("biotite.graphics members:", members)

# Load the structure
pdb_file = pdb.PDBFile.read("/home/ubuntu/rayca-artifacts/c2db8d53fb710fe21c5fee43/files/CRBN.pdb")
structure = pdb.get_structure(pdb_file, model=1)
print(f"\nStructure type: {type(structure)}")
print(f"Atoms: {len(structure)}")
print(f"Chains: {set(structure.chain_id)}")
print(f"Res range: {structure.res_id.min()} – {structure.res_id.max()}")
