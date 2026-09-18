
from Bio.PDB import Superimposer
from Bio import pairwise2
from Bio.SeqUtils import seq1

# Extract 1-letter sequences
def get_seq_and_ca(chain_residues):
    seq = "".join(seq1(r.get_resname()) for r in chain_residues)
    ca  = [r["CA"] for r in chain_residues]
    return seq, ca

ref_seq, ref_ca = get_seq_and_ca(ref_residues)

results = {}
for i in range(3):
    model_residues = [r for r in models[i][0]["B"].get_residues() if r.id[0]==" " and "CA" in r]
    mod_seq, mod_ca = get_seq_and_ca(model_residues)

    # Global pairwise alignment, allow gaps
    alns = pairwise2.align.globalms(ref_seq, mod_seq, 2, -1, -5, -0.5, one_alignment_only=True)
    aln_ref, aln_mod = alns[0].seqA, alns[0].seqB

    # Collect matched (non-gap) Cα pairs
    ref_atoms, mod_atoms = [], []
    ri = mi = 0
    for a, b in zip(aln_ref, aln_mod):
        if a != "-" and b != "-":
            ref_atoms.append(ref_ca[ri])
            mod_atoms.append(mod_ca[mi])
        if a != "-": ri += 1
        if b != "-": mi += 1

    # Superimpose
    sup = Superimposer()
    sup.set_atoms(ref_atoms, mod_atoms)
    rms = sup.rms

    # Also compute per-domain RMSD: thalidomide-binding domain (approx first 100 matched), rest
    n = len(ref_atoms)
    results[i] = {
        "n_matched": n,
        "rms_all": rms,
        "model_res_range": f"{model_residues[0].id[1]}–{model_residues[-1].id[1]}"
    }
    print(f"model_{i}: {n} matched Cα, RMSD = {rms:.3f} Å")

print("\nReference residues:", len(ref_residues), "| Crystal range: 47–427")
