
from Bio.SeqUtils import seq1
from Bio.PDB import Superimposer
from Bio import pairwise2
import numpy as np

def get_seq_and_ca(res_list):
    seq = "".join(seq1(r.get_resname()) for r in res_list)
    ca  = [r["CA"] for r in res_list]
    return seq, ca

# For each model: collect matched Cα pairs, then compute per-residue RMSD
# using the global superimposition, and also try splitting N/C halves
ref_seq, ref_ca = get_seq_and_ca(ref_residues)

for i in range(3):
    model_residues = [r for r in models[i][0]["B"].get_residues() if r.id[0]==" " and "CA" in r]
    mod_seq, mod_ca = get_seq_and_ca(model_residues)

    alns = pairwise2.align.globalms(ref_seq, mod_seq, 2, -1, -5, -0.5, one_alignment_only=True)
    aln_ref, aln_mod = alns[0].seqA, alns[0].seqB

    ref_atoms, mod_atoms = [], []
    ri = mi = 0
    for a, b in zip(aln_ref, aln_mod):
        if a != "-" and b != "-":
            ref_atoms.append(ref_ca[ri])
            mod_atoms.append(mod_ca[mi])
        if a != "-": ri += 1
        if b != "-": mi += 1

    n = len(ref_atoms)

    # Global superimposition — per-residue RMSD
    sup = Superimposer()
    sup.set_atoms(ref_atoms, mod_atoms)
    rot, tran = sup.rotran
    # transform model Cα coordinates
    ref_coords = np.array([a.get_vector().get_array() for a in ref_atoms])
    mod_coords = np.array([a.get_vector().get_array() for a in mod_atoms])
    mod_transformed = mod_coords @ rot.T + tran
    per_res = np.linalg.norm(ref_coords - mod_transformed, axis=1)

    # Domain split at midpoint
    mid = n // 2
    sup_n = Superimposer(); sup_n.set_atoms(ref_atoms[:mid], mod_atoms[:mid])
    sup_c = Superimposer(); sup_c.set_atoms(ref_atoms[mid:], mod_atoms[mid:])

    # tertile split
    t1, t2 = n//3, 2*n//3
    sup_t1 = Superimposer(); sup_t1.set_atoms(ref_atoms[:t1], mod_atoms[:t1])
    sup_t2 = Superimposer(); sup_t2.set_atoms(ref_atoms[t1:t2], mod_atoms[t1:t2])
    sup_t3 = Superimposer(); sup_t3.set_atoms(ref_atoms[t2:], mod_atoms[t2:])

    # worst 10 residues
    worst_idx = np.argsort(per_res)[-10:][::-1]
    worst_resids = [ref_residues[ri_].id[1] for ri_ in worst_idx]

    print(f"\n=== model_{i} ===")
    print(f"  Global RMSD ({n} Cα): {sup.rms:.2f} Å")
    print(f"  N-half RMSD ({mid} Cα): {sup_n.rms:.2f} Å")
    print(f"  C-half RMSD ({n-mid} Cα): {sup_c.rms:.2f} Å")
    print(f"  Tertile 1 RMSD ({t1} Cα): {sup_t1.rms:.2f} Å")
    print(f"  Tertile 2 RMSD ({t2-t1} Cα): {sup_t2.rms:.2f} Å")
    print(f"  Tertile 3 RMSD ({n-t2} Cα): {sup_t3.rms:.2f} Å")
    print(f"  Per-res dist: mean {per_res.mean():.2f} Å, median {np.median(per_res):.2f} Å, max {per_res.max():.2f} Å")
    print(f"  Fraction < 2 Å: {(per_res<2).mean()*100:.0f}%  < 5 Å: {(per_res<5).mean()*100:.0f}%")
    print(f"  Top-10 worst residues (crystal numbering): {worst_resids}")
