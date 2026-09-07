
print("Dispatching MD GBSA for EL2003A pose 2 ...")
print("  mode=md | nsteps=500000 (1 ns) | eqsteps=50000 | nframe=100")
print("  FF: amber03 protein / gaff2 ligand / AM1-BCC charges")
print("  method=gb | decompose=True | GPU=True")
print()

result_md = dispatch("gbsa", {
    "task":               "protein-ligand",
    "mode":               "md",
    "method":             "gb",
    "proteinFile":        "1Z5M_receptor_pH7.4.pdb",
    "ligandFile":         "EL2003A_pose2.sdf",
    "proteinForceField":  "amber03",
    "ligandForceField":   "gaff2",
    "ligandCharge":       "bcc",
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
