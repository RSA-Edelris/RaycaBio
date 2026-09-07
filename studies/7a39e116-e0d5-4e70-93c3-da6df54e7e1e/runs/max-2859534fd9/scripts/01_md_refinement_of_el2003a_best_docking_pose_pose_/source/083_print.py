
print("Retrying with ligandCharge='gas' (Gasteiger) — same fix that worked for the EM runs ...")

result_md = dispatch("gbsa", {
    "task":               "protein-ligand",
    "mode":               "md",
    "method":             "gb",
    "proteinFile":        "1Z5M_receptor_pH7.4.pdb",
    "ligandFile":         "EL2003A_pose2.sdf",
    "proteinForceField":  "amber03",
    "ligandForceField":   "gaff2",
    "ligandCharge":       "gas",
    "nsteps":             500000,
    "eqsteps":            50000,
    "nframe":             100,
    "decompose":          True,
    "threads":            8,
    "boxType":            "dodecahedron",
    "conc":               0.15,
}, files={
    "1Z5M_receptor_pH7.4.pdb": recep_file,
    "EL2003A_pose2.sdf":        pose_file,
}, gpu=True, timeout=3600)

print("rc:", result_md.get('rc'))
print("GPU:", result_md.get('gpu'))
print("Summary:", result_md.get('output', {}).get('summary', ''))
print("Best dG:", result_md.get('output', {}).get('best_dG_kcal_per_mol', ''))
