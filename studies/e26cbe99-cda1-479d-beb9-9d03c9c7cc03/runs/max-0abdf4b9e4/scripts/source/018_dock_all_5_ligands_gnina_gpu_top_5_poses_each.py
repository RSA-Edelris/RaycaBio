
# ── Dock all 5 ligands with gnina (GPU, top-5 poses each) ─────────────────────
docking_results = []

for name, lig_path in lig_sdf_paths:
    print(f"\n{'─'*60}")
    print(f"Docking {name} ...")
    r = dispatch('gnina', {
        'proteinFile':    trimmed_noh_path,
        'ligandFile':     lig_path,
        'boxX':           pocket_cx,
        'boxY':           pocket_cy,
        'boxZ':           pocket_cz,
        'width':          BOX_SZ,
        'height':         BOX_SZ,
        'depth':          BOX_SZ,
        'numModes':       5,
        'exhaustiveness': 16,
        'cnnScoring':     'rescore',
        'seed':           42,
    }, gpu=True)

    rc       = r.get('rc')
    best_aff = r.get('best_affinity_kcal_mol')
    best_cnn = r.get('best_cnn_affinity')
    best_pos = r.get('best_cnn_pose_score')
    n_poses  = r.get('num_poses')
    gpu_used = r.get('gpu_used')
    poses    = r.get('poses', [])
    out_file = r.get('output_file', '')

    print(f"  rc={rc}  gpu={gpu_used}  poses={n_poses}")
    print(f"  Best Vina affinity : {best_aff} kcal/mol")
    print(f"  Best CNN affinity  : {best_cnn} kcal/mol")
    print(f"  Best CNN pose score: {best_pos}")
    if poses:
        print("  All poses:")
        for p in poses:
            print(f"    mode {p.get('mode','?')}: "
                  f"vina={p.get('affinity_kcal_mol','?'):.2f}  "
                  f"cnn_aff={p.get('cnn_affinity','?'):.2f}  "
                  f"cnn_pose={p.get('cnn_pose_score','?'):.3f}")

    docking_results.append({
        'name':       name,
        'rc':         rc,
        'best_vina':  best_aff,
        'best_cnn':   best_cnn,
        'best_pose':  best_pos,
        'n_poses':    n_poses,
        'poses':      poses,
        'out_file':   out_file,
        'raw':        r,
    })

print(f"\n{'='*60}")
print(f"Docking complete for {len(docking_results)} ligands")
