
import os, shutil, gzip

receptor = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/receptor_CRBN_GSPT1.pdb"
lig_dir  = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/ligands"
pose_dir = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/poses"
os.makedirs(pose_dir, exist_ok=True)

cx, cy, cz = 12.758, -104.263, 27.873
bw = 22.0

compounds = [
    "lig_00_Compound_1.sdf",
    "lig_01_Compound_4.sdf",
    "lig_02_Compound_7.sdf",
    "lig_03_Compound_8.sdf",
    "lig_04_Compound_9.sdf",
    "lig_05_Compound_10.sdf",
    "lig_06_Compound_11.sdf",
    "lig_07_Compound_12.sdf",
]

summary_rows = []

for lig_fname in compounds:
    cname = lig_fname.replace("lig_0","").replace("_"," ").replace(".sdf","").strip()
    # Get scores from previous run
    r  = results[lig_fname]
    op = r['output']
    poses = op['poses']
    top_p1 = poses[0]  # CNN-ranked top pose
    best_emp = min(p['affinity'] for p in poses)  # best empirical affinity

    summary_rows.append({
        'name':          cname,
        'fname':         lig_fname,
        'n_poses':       op['num_poses'],
        'top_cnn_pose':  op['best_cnn_pose_score'],
        'top_cnn_aff':   op['best_cnn_affinity'],
        'top_emp_aff':   top_p1['affinity'],
        'best_emp_aff':  best_emp,
        'poses':         poses,
    })
    print(f"{cname:15s}  CNN_pose={op['best_cnn_pose_score']:.3f}  CNN_aff={op['best_cnn_affinity']:.2f}  "
          f"emp_top={top_p1['affinity']:.2f}  emp_best={best_emp:.2f} kcal/mol")

print("\n--- Re-docking each compound and saving pose SDF ---")
for row in summary_rows:
    lig_path   = os.path.join(lig_dir, row['fname'])
    out_gz     = os.path.join(pose_dir, row['fname'].replace('.sdf', '_poses.sdf.gz'))
    out_sdf    = out_gz.replace('.gz', '')

    r2 = run_aidd_tool('gnina', {
        'proteinFile':   receptor,
        'ligandFile':    lig_path,
        'boxX': cx, 'boxY': cy, 'boxZ': cz,
        'width': bw, 'height': bw, 'depth': bw,
        'cnnScoring':    'rescore',
        'exhaustiveness': 16,
        'numModes':      9,
        'seed':          42,
    })

    # gnina writes gnina_docked.sdf.gz to workspace; copy it out
    ws_gz = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/gnina_docked.sdf.gz"
    if os.path.exists(ws_gz):
        with gzip.open(ws_gz, 'rb') as fin, open(out_sdf, 'wb') as fout:
            fout.write(fin.read())
        os.remove(ws_gz)
        print(f"  Saved: {os.path.basename(out_sdf)}")
    else:
        print(f"  WARNING: no output file for {row['name']}")
