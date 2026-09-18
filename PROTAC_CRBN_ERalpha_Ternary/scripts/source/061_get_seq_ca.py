
from Bio.SeqUtils import seq1
import numpy as np

def get_seq_and_ca(res_list):
    seq = "".join(seq1(r.get_resname()) for r in res_list)
    ca  = [r["CA"] for r in res_list]
    return seq, ca

# ---- check sequence identity for model_0 alignment ----
model_residues = [r for r in models[0][0]["B"].get_residues() if r.id[0]==" " and "CA" in r]
ref_seq, ref_ca   = get_seq_and_ca(ref_residues)
mod_seq, mod_ca   = get_seq_and_ca(model_residues)

from Bio import pairwise2
alns = pairwise2.align.globalms(ref_seq, mod_seq, 2, -1, -5, -0.5, one_alignment_only=True)
aln_ref, aln_mod = alns[0].seqA, alns[0].seqB

matches = sum(a==b for a,b in zip(aln_ref, aln_mod) if a!="-" and b!="-")
aligned  = sum(1 for a,b in zip(aln_ref,aln_mod) if a!="-" and b!="-")
print(f"Sequence identity: {matches}/{aligned} = {matches/aligned*100:.1f}%")
print(f"Alignment length: {len(aln_ref)}, gaps in ref: {aln_ref.count('-')}, gaps in model: {aln_mod.count('-')}")
print(f"First 60 ref:   {aln_ref[:60]}")
print(f"First 60 model: {aln_mod[:60]}")
print(f"Last  40 ref:   {aln_ref[-40:]}")
print(f"Last  40 model: {aln_mod[-40:]}")
