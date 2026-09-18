
from Bio.SeqUtils import seq1
from Bio.PDB import Superimposer
import numpy as np

def get_seq_ca(res_list):
    seq = "".join(seq1(r.get_resname()) for r in res_list)
    ca  = [r["CA"] for r in res_list]
    return seq, ca

ref_seq, ref_ca = get_seq_ca(ref_residues)

# Check if crystal is a contiguous substring of any model
model_residues_0 = [r for r in models[0][0]["B"].get_residues() if r.id[0]==" " and "CA" in r]
mod_seq_0, _     = get_seq_ca(model_residues_0)

pos = mod_seq_0.find(ref_seq)
print(f"Crystal seq as exact substring of model: start={pos}")

# Crystal has gaps (disordered loops) — so it may NOT be a perfect substring.
# Find best ungapped local alignment window via Smith-Waterman
from Bio import pairwise2
local_alns = pairwise2.align.localms(ref_seq, mod_seq_0, 2, -1, -5, -0.5, one_alignment_only=True)
laln_ref, laln_mod = local_alns[0].seqA, local_alns[0].seqB

# Find start offset in model sequence by counting non-gap characters before the local alignment start
# pairwise2 local alignment gives begin/end positions
print(f"Local aln score: {local_alns[0].score:.0f}")
print(f"Local aln begin/end: ref [{local_alns[0].start},{local_alns[0].end}]")

# Count gaps at start of local_mod (these are model residues BEFORE the match starts)
# local alignment trims leading/trailing gaps
# Check model offset by re-aligning with start/end indices
print(f"First 40 aln_ref: {laln_ref[:40]}")
print(f"First 40 aln_mod: {laln_mod[:40]}")
print(f"Last  30 aln_ref: {laln_ref[-30:]}")
print(f"Last  30 aln_mod: {laln_mod[-30:]}")
