
# ── Ternary pose ensemble sampling + linker cooperativity scoring ──
# For each of 4 linker lengths:
#   - Sample N random perturbations of BD1 around the reference (superposed) position
#   - For each pose: compute exit-to-exit distance d(pose) and interface contacts
#   - Weight by Gaussian-chain linker probability P_L(d) ∝ d² exp(-3d²/(2nb²))
#   - Effective cooperativity proxy ∝ sum_pose [ contacts(pose) × P_L(d(pose)) ]

def apply_transform(c,R,t): return c@R.T+t

np.random.seed(42)
N_SAMPLES = 5000
BOND_LEN   = 1.5   # Å per heavy atom

# Linker definitions: (label, n_heavy_atoms, description)
linkers = [
    ("L1-short",    4,  "~C4 alkyl, 2-atom ether"),
    ("L2-medium",   8,  "PEG2-like, 8 atoms"),
    ("L3-long",     12, "PEG3/PEG4-like (~MZ1), 12 atoms"),
    ("L4-xlong",    18, "PEG5-PEG6, 18 atoms"),
]

# Reference: BD1 CA coords (transformed) and JQ1 exit coords (transformed)
# jq1_exit_tf: JQ1 exit atom transformed to ternary frame (already computed)
# vhl_exit_xyz: VHL warhead exit atom in 5T35 frame
# bd1_ca_tf: BD1 Cα in ternary frame
# vhl_ca: VHL Cα in 5T35 frame

def read_ca_chain(path, chain_id):
    c=[]; seen=set()
    with open(path) as f:
        for line in f:
            if line[:4]=="ATOM" and line[21]==chain_id and line[12:16].strip()=="CA":
                rn=int(line[22:26])
                if rn not in seen:
                    seen.add(rn)
                    x,y,z=float(line[30:38]),float(line[38:46]),float(line[46:54])
                    c.append(np.array([x,y,z]))
    return np.array(c)

bd1_ca_tf_arr = apply_transform(read_ca_chain(pdb3,'A'), Rf, tf)
vhl_ca_arr    = read_ca_chain(pdb5,'D')
bd1_cen       = bd1_ca_tf_arr.mean(axis=0)

def rot_matrix_from_axisangle(axis, angle):
    """Rodrigues' rotation formula."""
    axis = axis / np.linalg.norm(axis)
    c, s = np.cos(angle), np.sin(angle)
    K = np.array([[0,-axis[2],axis[1]],[axis[2],0,-axis[0]],[-axis[1],axis[0],0]])
    return np.eye(3) + s*K + (1-c)*(K@K)

def gaussian_linker_prob(d, n, b=BOND_LEN):
    """Unnormalized Gaussian-chain probability at distance d with n atoms."""
    if n <= 0: return 0.0
    sigma2 = n * b**2 / 3.0
    return d**2 * np.exp(-d**2 / (2*sigma2))

def count_interface_ca(ca1, ca2, cutoff=8.0):
    n = 0
    for a in ca1:
        n += (np.linalg.norm(ca2 - a, axis=1) < cutoff).sum()
    return n

def max_extension(n, b=BOND_LEN):
    return n * b

results = {}
for label, n_atoms, desc in linkers:
    max_ext = max_extension(n_atoms)
    scores = []
    for _ in range(N_SAMPLES):
        # Small rotation around random axis, up to ±15°
        axis  = np.random.randn(3)
        angle = np.random.uniform(-np.pi/12, np.pi/12)
        R_pert = rot_matrix_from_axisangle(axis, angle)
        trans  = np.random.randn(3) * 1.5  # ±1.5 Å translation

        # Perturb BD1 CA and JQ1 exit
        bd1_ca_pert    = (bd1_ca_tf_arr - bd1_cen) @ R_pert.T + bd1_cen + trans
        jq1_exit_pert  = R_pert @ (jq1_exit_tf - bd1_cen) + bd1_cen + trans

        # Exit-to-exit distance in this pose
        d = float(np.linalg.norm(jq1_exit_pert - vhl_exit_xyz))

        # Skip if linker cannot physically reach (max extension < d)
        # or if distance is below meaningful minimum (2 Å)
        if d > max_ext or d < 2.0:
            continue

        # Linker probability
        p_linker = gaussian_linker_prob(d, n_atoms)

        # Interface contacts (Cα-Cα < 8 Å)
        n_contacts = count_interface_ca(bd1_ca_pert, vhl_ca_arr, cutoff=8.0)

        scores.append(p_linker * n_contacts)

    results[label] = {
        'n_atoms':   n_atoms,
        'desc':      desc,
        'max_ext':   max_ext,
        'n_poses':   len(scores),
        'mean_score': np.mean(scores) if scores else 0.0,
        'total_score': np.sum(scores),
    }

# Reference d for direct reporting
d_ref = bd1_exit_to_vhl_exit  # 5.6 Å
print(f"Required bridging distance (BD1→VHL exit): {d_ref:.1f} Å\n")
print(f"{'Linker':<14} {'n_atoms':>7} {'max_ext(Å)':>10} {'n_poses':>8} "
      f"{'P_link@d_ref':>13} {'mean_score':>11} {'rank':>5}")
print("-"*72)

for label, n_atoms, desc in linkers:
    r = results[label]
    p_at_ref = gaussian_linker_prob(d_ref, n_atoms)
    print(f"{label:<14} {n_atoms:>7} {r['max_ext']:>10.1f} {r['n_poses']:>8} "
          f"{p_at_ref:>13.4f} {r['mean_score']:>11.4f}")
