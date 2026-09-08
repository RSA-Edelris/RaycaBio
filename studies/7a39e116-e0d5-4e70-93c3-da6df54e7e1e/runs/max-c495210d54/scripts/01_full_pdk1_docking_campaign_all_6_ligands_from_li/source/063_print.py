
import json, os

receptor_path = f"{ART}/1Z5M_receptor_pH7.4.pdb"
poses_dir_path = f"{ART}/all_poses"

gbsa_all = {}   # lig_name -> result dict

for lig_name in ligand_names:
    print(f"\n{'='*60}")
    print(f"MM-GBSA: {lig_name} (5 poses, mode=em, gaff2+amber03, bcc)")
    
    # Build file list for all 5 poses
    pose_files = {}
    lig_file_keys = []
    for rank in range(1, 6):
        key = f"{lig_name}_pose{rank}.sdf"
        # Write individual pose SDF
        pose_sdf_path = f"{poses_dir_path}/{key}"
        pose_r = [r for r in pose_table if r['mol_name'] == lig_name and r['rank'] == rank][0]
        with open(pose_sdf_path, 'w') as fh:
            fh.write(pose_r['block'] + '\n$$$$\n')
        pose_files[key] = pose_sdf_path
        lig_file_keys.append(key)
    
    files_dict = {"1Z5M_receptor_pH7.4.pdb": receptor_path}
    files_dict.update(pose_files)
    
    res = dispatch("gbsa", {
        "task": "protein-ligand",
        "mode": "em",
        "method": "gb",
        "proteinFile": "1Z5M_receptor_pH7.4.pdb",
        "ligandFiles": lig_file_keys,
        "proteinForceField": "amber03",
        "ligandForceField": "gaff2",
        "ligandCharge": "gas",
        "threads": 8,
        "decompose": True
    }, files=files_dict, gpu=True, timeout=1800)
    
    rc = res.get("rc", -1)
    out = res.get("output", {})
    print(f"  rc={rc}  best_dG={out.get('best_dG_kcal_per_mol')}  gpu={out.get('gpu')}")
    if rc != 0:
        print(f"  ERROR: {res.get('summary','')[:300]}")
    
    gbsa_all[lig_name] = {'rc': rc, 'output': out, 'results': out.get('results', [])}
    
    # Save intermediate result
    with open(f"{ART}/gbsa_{lig_name}.json", 'w') as fh:
        json.dump(gbsa_all[lig_name], fh, indent=2)
    print(f"  Saved gbsa_{lig_name}.json")

print("\n=== All GBSA jobs complete ===")
