
from Bio import PDB
from Bio.PDB import PDBParser, Superimposer
import numpy as np

parser = PDBParser(QUIET=True)

SESSION = "/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74"
REF_PDB = "/home/ubuntu/rayca-artifacts/c2db8d53fb710fe21c5fee43/files/CRBN.pdb"

# Load reference crystal CRBN (chain B)
ref_struct = parser.get_structure("CRBN_xtal", REF_PDB)
ref_chain = ref_struct[0]["B"]

# Get Cα atoms from reference (ATOM only, no HETATM)
ref_residues = [r for r in ref_chain.get_residues() if r.id[0] == " " and "CA" in r]
ref_seq_nums = [r.id[1] for r in ref_residues]
print(f"Reference CRBN: chain B, {len(ref_residues)} residues, range {ref_seq_nums[0]}–{ref_seq_nums[-1]}")

# Load the 3 ARV-471 Boltz-2 models; CRBN is chain B in each
models = {}
for i in range(3):
    path = f"{SESSION}/ARV471_ERalpha_CRBN_model_{i}.pdb"
    s = parser.get_structure(f"model_{i}", path)
    chains = [c.id for c in s[0].get_chains()]
    crbn_res = [r for r in s[0]["B"].get_residues() if r.id[0] == " " and "CA" in r]
    print(f"  model_{i}: chains {chains}, CRBN residues {len(crbn_res)} (1-indexed, range {crbn_res[0].id[1]}–{crbn_res[-1].id[1]})")
    models[i] = s
