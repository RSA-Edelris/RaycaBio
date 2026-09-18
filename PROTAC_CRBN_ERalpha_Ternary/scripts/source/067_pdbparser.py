
from Bio.PDB import PDBParser, Superimposer
from Bio.SeqUtils import seq1
from Bio import pairwise2
import numpy as np

SESSION = "/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74"
REF_PDB = "/home/ubuntu/rayca-artifacts/c2db8d53fb710fe21c5fee43/files/CRBN.pdb"

parser = PDBParser(QUIET=True)

# Load reference (chain B, standard residues only)
ref_struct = parser.get_structure("CRBN_xtal", REF_PDB)
ref_chain = ref_struct[0]["B"]
ref_residues = [r for r in ref_chain.get_residues() if r.id[0] == " " and "CA" in r]
print(f"Reference CRBN: {len(ref_residues)} Cα residues (residues {ref_residues[0].id[1]}–{ref_residues[-1].id[1]})")

# Load 3 Boltz-2 ARV-471 models (chain B = CRBN)
models = []
for i in range(3):
    s = parser.get_structure(f"model_{i}", f"{SESSION}/ARV471_ERalpha_CRBN_model_{i}.pdb")
    models.append(s)
    chain_b = s[0]["B"]
    res = [r for r in chain_b.get_residues() if r.id[0] == " " and "CA" in r]
    print(f"model_{i} chain B: {len(res)} Cα residues")
