
from Bio.SeqUtils import seq1
from Bio.PDB import Superimposer
from Bio import pairwise2
import numpy as np

def get_seq_ca(res_list):
    seq = "".join(seq1(r.get_resname()) for r in res_list)
    ca  = [r["CA"] for r in res_list]
    return seq, ca

ref_seq, ref_ca = get_seq_ca(ref_residues)

# CRBN domain boundaries in native (crystal) numbering:
# LON-homology (N-lobe):   47 ~165   (helical repeats)
# LON-homology (C-lobe): 166 ~320
# Thalidomide-binding domain (TBD / CULT): 321~427
DOMAIN_CUTS = {
    "N-lobe (47–165)":   (47, 165),
    "C-lobe (166–320)":  (166, 320),
    "TBD   (321–427)":   (321, 427),
}

for i in range(3):
    model_res = [r for r in models[i][0]["B"].get_residues() if r.id[0]==" " and "CA" in r]
    mod_seq, mod_ca = get_seq_ca(model_res)

    alns = pairwise2.align.localms(ref_seq, mod_seq, 2, -1, -5, -0.5, one_alignment_only=True)
    laln_ref, laln_mod = alns[0].seqA, alns[0].seqB

    ref_atoms, mod_atoms, ref_resnums = [], [], []
    ri = mi = 0
    for a, b in zip(laln_ref, laln_mod):
        if a != "-" and b != "-":
            ref_atoms.append(ref_ca[ri]); mod_atoms.append(mod_ca[mi])
            ref_resnums.append(ref_residues[ri].id[1])
        if a != "-": ri += 1
        if b != "-": mi += 1

    ref_resnums = np.array(ref_resnums)
    print(f"\n=== model_{i} — per-domain RMSD ===")
    for dname, (lo, hi) in DOMAIN_CUTS.items():
        mask = (ref_resnums >= lo) & (ref_resnums <= hi)
        if mask.sum() < 10:
            print(f"  {dname}: too few residues ({mask.sum()})")
            continue
        ra = [ref_atoms[j] for j in np.where(mask)[0]]
        ma = [mod_atoms[j] for j in np.where(mask)[0]]
        sup = Superimposer(); sup.set_atoms(ra, ma)
        print(f"  {dname}: {mask.sum()} Cα, RMSD = {sup.rms:.2f} Å")

    # pLDDT from B-factor of model CRBN chain
    plddt_vals = []
    for r in models[i][0]["B"].get_residues():
        if r.id[0]==" " and "CA" in r:
            plddt_vals.append(r["CA"].get_bfactor())
    plddt = np.array(plddt_vals)
    print(f"  pLDDT (B-factor): mean {plddt.mean():.1f}, min {plddt.min():.1f}, max {plddt.max():.1f}")
    # TBD region pLDDT — approximate model positions for last ~100 residues
    print(f"  pLDDT last 107 (≈TBD): mean {plddt[-107:].mean():.1f}")
    print(f"  pLDDT first 180 (≈N-lobe): mean {plddt[:180].mean():.1f}")
