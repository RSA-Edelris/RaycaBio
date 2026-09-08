
# Stage all 5 clean poses + receptor
all_files = {
    "1Z5M_receptor_pH7.4.pdb": f"{ART}/1Z5M_receptor_pH7.4.pdb",
}
for i in range(1, 6):
    key = f"clean_pose_{i}.sdf"
    # Clean files are in workspace (written above, now also in ART)
    path = f"{WS}/clean_pose_{i}.sdf"
    all_files[key] = path

print("Staging files:", list(all_files.keys()))
print("\nDispatching gbsa for all 5 poses (em mode)...")

result_all = dispatch("gbsa", {
    "task": "protein-ligand",
    "mode": "em",
    "method": "gb",
    "proteinFile": "1Z5M_receptor_pH7.4.pdb",
    "ligandFiles": [f"clean_pose_{i}.sdf" for i in range(1,6)],
    "proteinForceField": "amber03",
    "ligandForceField": "gaff2",
    "ligandCharge": "gas",
    "threads": 8,
    "decompose": True    # per-residue decomposition
}, files=all_files, gpu=True, timeout=1800)

print("rc:", result_all.get("rc"))
print("summary:", result_all.get("summary",""))
out_all = result_all.get("output", {})
print("best_dG:", out_all.get("best_dG_kcal_per_mol"))
print("\nAll results:")
for r in (out_all.get("results") or []):
    print(f"  {r.get('ligandName')}: dG={r.get('TOTAL','?')} kcal/mol  "
          f"VdW={r.get('Van der Waals','?')}  Elec={r.get('Electrostatic','?')}  "
          f"Polar={r.get('Polar Solvation','?')}")
