
receptor = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/receptor_CRBN_GSPT1.pdb"
lig_dir  = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/ligands"

# Box: center on 85C centroid, 22 Å cube
cx, cy, cz = 12.758, -104.263, 27.873
bw = 22.0

import os, time

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

results = {}
for lig_fname in compounds:
    name = lig_fname.replace("lig_0", "").replace("_", " ").replace(".sdf","").strip()
    lig_path = os.path.join(lig_dir, lig_fname)
    print(f"\nDocking {lig_fname} ...")
    t0 = time.time()
    r = run_aidd_tool('gnina', {
        'proteinFile': receptor,
        'ligandFile':  lig_path,
        'boxX': cx, 'boxY': cy, 'boxZ': cz,
        'width': bw, 'height': bw, 'depth': bw,
        'cnnScoring': 'rescore',
        'exhaustiveness': 16,
        'numModes': 9,
        'seed': 42,
    })
    dt = time.time() - t0
    results[lig_fname] = r
    if isinstance(r, dict):
        aff  = r.get('best_affinity_kcal_mol', 'N/A')
        cnn  = r.get('best_cnn_affinity', 'N/A')
        pose = r.get('best_cnn_pose_score', 'N/A')
        gpu  = r.get('gpu_used', '?')
        n    = r.get('num_poses', '?')
        print(f"  affinity={aff} kcal/mol  cnn_aff={cnn}  cnn_pose={pose}  gpu={gpu}  poses={n}  [{dt:.0f}s]")
    else:
        print(f"  ERROR: {r}")

print("\n=== DOCKING COMPLETE ===")
