
from Bio.SeqUtils import seq1
from Bio.PDB import Superimposer
from Bio import pairwise2
import numpy as np

def get_seq_ca(res_list):
    seq = "".join(seq1(r.get_resname()) for r in res_list)
    ca  = [r["CA"] for r in res_list]
    return seq, ca

ref_seq, ref_ca = get_seq_ca(ref_residues)

report = []

for i in range(3):
    model_res = [r for r in models[i][0]["B"].get_residues() if r.id[0]==" " and "CA" in r]
    mod_seq, mod_ca = get_seq_ca(model_res)

    # Use LOCAL alignment to find the correct window
    alns = pairwise2.align.localms(ref_seq, mod_seq, 2, -1, -5, -0.5, one_alignment_only=True)
    laln_ref, laln_mod = alns[0].seqA, alns[0].seqB

    # Build paired Cα lists from alignment (skip leading/trailing '-' in ref)
    ref_atoms, mod_atoms = [], []
    ref_resids_matched = []   # crystal residue numbers for reporting
    ri = mi = 0
    in_local = False
    for a, b in zip(laln_ref, laln_mod):
        if a != "-":
            in_local = True
        if in_local and a == "-" and b != "-":
            # model residue with no crystal counterpart (C-terminal overhang)
            mi += 1
            continue
        if a != "-" and b != "-":
            ref_atoms.append(ref_ca[ri])
            mod_atoms.append(mod_ca[mi])
            ref_resids_matched.append(ref_residues[ri].id[1])
        if a != "-": ri += 1
        if b != "-": mi += 1

    n = len(ref_atoms)

    # Global superimposition on correctly matched pairs
    sup_all = Superimposer()
    sup_all.set_atoms(ref_atoms, mod_atoms)
    rot, tran = sup_all.rotran

    ref_coords = np.array([a.get_vector().get_array() for a in ref_atoms])
    mod_coords = np.array([a.get_vector().get_array() for a in mod_atoms])
    mod_xfm    = mod_coords @ rot.T + tran
    per_res    = np.linalg.norm(ref_coords - mod_xfm, axis=1)

    # Halves
    mid = n // 2
    sup_n = Superimposer(); sup_n.set_atoms(ref_atoms[:mid], mod_atoms[:mid])
    sup_c = Superimposer(); sup_c.set_atoms(ref_atoms[mid:], mod_atoms[mid:])

    # Pocket residues: near the LVY ligand (CRBN triazide pocket ~135-145, 380-400)
    pocket_resids = set(range(127, 165)) | set(range(374, 410))
    pocket_mask = np.array([r in pocket_resids for r in ref_resids_matched])

    pock_rmsd = np.sqrt(np.mean(per_res[pocket_mask]**2)) if pocket_mask.any() else float('nan')

    print(f"\n=== model_{i} ===")
    print(f"  Matched Cα pairs (local aln): {n}")
    print(f"  Full-chain RMSD:   {sup_all.rms:.2f} Å")
    print(f"  N-half RMSD ({mid}): {sup_n.rms:.2f} Å  |  C-half RMSD ({n-mid}): {sup_c.rms:.2f} Å")
    print(f"  Per-res: mean {per_res.mean():.2f} Å  median {np.median(per_res):.2f} Å  max {per_res.max():.2f} Å")
    print(f"  < 2 Å: {(per_res<2).mean()*100:.0f}%   < 3 Å: {(per_res<3).mean()*100:.0f}%   < 5 Å: {(per_res<5).mean()*100:.0f}%")
    print(f"  Pocket-residue RMSD ({pocket_mask.sum()} Cα): {pock_rmsd:.2f} Å")
    worst = np.argsort(per_res)[-5:][::-1]
    print(f"  5 worst (crystal res): { [(ref_resids_matched[j], f'{per_res[j]:.1f}Å') for j in worst] }")
    best  = np.argsort(per_res)[:5]
    print(f"  5 best  (crystal res): { [(ref_resids_matched[j], f'{per_res[j]:.2f}Å') for j in best] }")
    report.append((i, sup_all.rms, sup_n.rms, sup_c.rms, pock_rmsd, per_res))
