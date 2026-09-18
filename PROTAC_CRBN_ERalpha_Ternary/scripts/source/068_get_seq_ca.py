
from Bio.SeqUtils import seq1

def get_seq_ca(res_list):
    seq = "".join(seq1(r.get_resname()) for r in res_list)
    ca  = [r["CA"] for r in res_list]
    return seq, ca

ref_seq, ref_ca = get_seq_ca(ref_residues)

DOMAIN_CUTS = {
    "N-lobe (47–165)":  (47, 165),
    "C-lobe (166–320)": (166, 320),
    "TBD (321–427)":    (321, 427),
}

# Pocket residues near LVY ligand
pocket_resids = set(range(127, 165)) | set(range(374, 410))

results = []

for i in range(3):
    model_res = [r for r in models[i][0]["B"].get_residues() if r.id[0] == " " and "CA" in r]
    mod_seq, mod_ca = get_seq_ca(model_res)

    # Local alignment to find correct window
    alns = pairwise2.align.localms(ref_seq, mod_seq, 2, -1, -5, -0.5, one_alignment_only=True)
    laln_ref, laln_mod = alns[0].seqA, alns[0].seqB

    ref_atoms, mod_atoms, ref_resids_matched, ref_resnums = [], [], [], []
    ri = mi = 0
    for a, b in zip(laln_ref, laln_mod):
        if a != "-" and b != "-":
            ref_atoms.append(ref_ca[ri])
            mod_atoms.append(mod_ca[mi])
            ref_resids_matched.append(ref_residues[ri].id[1])
            ref_resnums.append(ref_residues[ri].id[1])
        if a != "-": ri += 1
        if b != "-": mi += 1

    n = len(ref_atoms)
    ref_resnums = np.array(ref_resnums)

    # Global superimposition
    sup_all = Superimposer()
    sup_all.set_atoms(ref_atoms, mod_atoms)
    rot, tran = sup_all.rotran

    ref_coords = np.array([a.get_vector().get_array() for a in ref_atoms])
    mod_coords = np.array([a.get_vector().get_array() for a in mod_atoms])

    # CORRECTED: rot (not rot.T)
    mod_xfm  = mod_coords @ rot + tran
    per_res  = np.linalg.norm(ref_coords - mod_xfm, axis=1)

    # Sanity check: Jensen's inequality must hold (mean ≤ RMSD)
    rmsd_check = sup_all.rms
    mean_dist  = per_res.mean()
    jensen_ok  = mean_dist <= rmsd_check + 1e-6
    # Also: RMSD from scratch should equal sup.rms
    rmsd_scratch = np.sqrt(np.mean(per_res**2))

    # Pocket mask
    pocket_mask = np.array([r in pocket_resids for r in ref_resids_matched])
    pock_rmsd   = np.sqrt(np.mean(per_res[pocket_mask]**2)) if pocket_mask.any() else float('nan')

    # Domain RMSDs (using sup.rms — unchanged from 065)
    domain_rmsds = {}
    for dname, (lo, hi) in DOMAIN_CUTS.items():
        mask = (ref_resnums >= lo) & (ref_resnums <= hi)
        if mask.sum() < 10:
            domain_rmsds[dname] = None
            continue
        ra = [ref_atoms[j] for j in np.where(mask)[0]]
        ma = [mod_atoms[j] for j in np.where(mask)[0]]
        sup_d = Superimposer(); sup_d.set_atoms(ra, ma)
        domain_rmsds[dname] = (mask.sum(), sup_d.rms)

    # pLDDT from B-factor of full model chain B (all 469 residues)
    plddt_all = np.array([r["CA"].get_bfactor()
                          for r in models[i][0]["B"].get_residues()
                          if r.id[0] == " " and "CA" in r])

    # pLDDT for matched (crystal-equivalent) residues only
    # model positions in the matched window: get the model-side residue indices
    # The matched window starts at model position ~70 (tag) and covers 370 residues
    # Use model_res list and find which positions are matched
    mi2 = 0; match_model_idx = []
    ri2 = 0
    for a, b in zip(laln_ref, laln_mod):
        if a != "-" and b != "-":
            match_model_idx.append(mi2)
        if a != "-": ri2 += 1
        if b != "-": mi2 += 1

    plddt_matched = np.array([model_res[j]["CA"].get_bfactor() for j in match_model_idx])

    print(f"\n=== model_{i} (CORRECTED) ===")
    print(f"  Matched Cα pairs: {n}")
    print(f"  Global RMSD (sup.rms):  {rmsd_check:.2f} Å")
    print(f"  Global RMSD (recomputed from corrected coords): {rmsd_scratch:.4f} Å  [should match sup.rms]")
    print(f"  Jensen check (mean ≤ RMSD): mean={mean_dist:.2f} Å  → {'OK' if jensen_ok else 'FAIL'}")
    print(f"  Per-res: mean {mean_dist:.2f} Å  median {np.median(per_res):.2f} Å  max {per_res.max():.2f} Å")
    print(f"  < 2 Å: {(per_res<2).mean()*100:.0f}%   < 3 Å: {(per_res<3).mean()*100:.0f}%   < 5 Å: {(per_res<5).mean()*100:.0f}%")
    print(f"  Pocket-residue RMSD ({pocket_mask.sum()} Cα): {pock_rmsd:.2f} Å")
    worst = np.argsort(per_res)[-5:][::-1]
    print(f"  5 worst (crystal res): {[(ref_resids_matched[j], f'{per_res[j]:.1f}Å') for j in worst]}")
    best = np.argsort(per_res)[:5]
    print(f"  5 best  (crystal res): {[(ref_resids_matched[j], f'{per_res[j]:.2f}Å') for j in best]}")
    print(f"  Domain RMSDs:")
    for dname, val in domain_rmsds.items():
        if val:
            print(f"    {dname}: {val[0]} Cα, {val[1]:.2f} Å")
    print(f"  pLDDT (matched 370 residues): mean {plddt_matched.mean():.1f}  min {plddt_matched.min():.1f}  max {plddt_matched.max():.1f}")
    print(f"  pLDDT (all 469 model residues): mean {plddt_all.mean():.1f}  min {plddt_all.min():.1f}  max {plddt_all.max():.1f}")

    results.append({
        "model": i, "n": n, "rmsd": rmsd_check,
        "mean": mean_dist, "median": float(np.median(per_res)), "max": float(per_res.max()),
        "lt2": float((per_res<2).mean()*100), "lt3": float((per_res<3).mean()*100),
        "lt5": float((per_res<5).mean()*100),
        "pock_rmsd": pock_rmsd, "n_pocket": int(pocket_mask.sum()),
        "domain_rmsds": domain_rmsds,
        "plddt_matched_mean": float(plddt_matched.mean()),
        "per_res": per_res,
    })
