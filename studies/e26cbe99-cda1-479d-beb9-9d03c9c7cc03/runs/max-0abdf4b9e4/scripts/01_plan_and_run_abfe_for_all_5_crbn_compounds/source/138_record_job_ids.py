
# Record job IDs
jobs = {
    "complex_EDS01806218_ent1": "6324320",
    "complex_EDS01806218_ent2": "6324332",
    "complex_EDS01889984":      "6324347",
    "solvent_EDS01806218_ent1": "6324357",
    "solvent_EDS01806218_ent2": "6324401",
    "solvent_EDS01889984":      "6324414",
    "md_EDS01357518_ent2":      "6324421",
}

import json
with open(f"{BASE}/abfe_job_ids.json", "w") as f:
    json.dump(jobs, f, indent=2)

print("ABFE jobs submitted to Isambard:")
print(f"{'Job type':<35} {'SLURM ID':>10}  {'Walltime':>10}")
print("-" * 60)
for k, jid in jobs.items():
    wt = "240 min" if k.startswith("complex") else ("150 min" if "357518" in k else "120 min")
    print(f"  {k:<33} {jid:>10}  {wt:>10}")

# Analytical Boresch corrections (precomputed)
boresch = {
    "EDS01806218_ent1": 7.33,
    "EDS01806218_ent2": 7.36,
    "EDS01889984":      7.89,
}
print(f"\nBoresch ΔG_restr corrections (kcal/mol):")
for k, v in boresch.items():
    print(f"  {k}: {v:.2f}")
