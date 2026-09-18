
from helpers import kabsch, apply_transform, rmsd

# BD1 has 127 res (42-168), BD2 has 111 res (349-459)
# Try aligning last 111 of BD1 (res 58-168) to BD2 — skips N-terminal linker
bd1_res_last111 = bd1_res[16:]   # res 58-168
mobile_arr2 = np.array([bd1_ca[r] for r in bd1_res_last111])
target_arr2 = np.array([bd2_ca[r] for r in bd2_res])

R2, t2 = kabsch(mobile_arr2, target_arr2)
fit2 = apply_transform(mobile_arr2, R2, t2)
print(f"Aligned last 111 res of BD1 → BD2:  RMSD = {rmsd(fit2, target_arr2):.2f} Å")

# Iterative trimming: remove pairs >2σ from mean deviation, re-fit
pairs_mobile = mobile_arr2.copy()
pairs_target = target_arr2.copy()
for iteration in range(8):
    R_it, t_it = kabsch(pairs_mobile, pairs_target)
    fit_it = apply_transform(pairs_mobile, R_it, t_it)
    dists = np.sqrt(np.sum((fit_it - pairs_target)**2, axis=1))
    cutoff = dists.mean() + 2 * dists.std()
    keep = dists <= cutoff
    pairs_mobile = pairs_mobile[keep]
    pairs_target = pairs_target[keep]
    r = rmsd(apply_transform(pairs_mobile, R_it, t_it), pairs_target)
    print(f"  iter {iteration+1}: {keep.sum()} pairs, RMSD = {r:.2f} Å")
    if keep.all():
        break

R_final, t_final = kabsch(pairs_mobile, pairs_target)
fit_final = apply_transform(pairs_mobile, R_final, t_final)
print(f"\nFinal core RMSD: {rmsd(fit_final, pairs_target):.2f} Å over {len(pairs_mobile)} residues")
print("Transform R:\n", R_final)
print("t:", t_final)
