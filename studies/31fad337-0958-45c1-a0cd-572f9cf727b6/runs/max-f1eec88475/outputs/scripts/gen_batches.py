#!/usr/bin/env python3
"""Generate 9 MM-GBSA batch scripts."""
import json
from pathlib import Path

WDIR = Path("/home/ubuntu/rayca-sessions/31fad337-0958-45c1-a0cd-572f9cf727b6-0505c6de016f/cdk2_campaign")
REC  = str(WDIR / "receptor_gromacs_ready.pdb")

paths = json.loads((WDIR / "gbsa_lig_paths.json").read_text())
print(f"Total ligands: {len(paths)}")

N_BATCHES = 9
batch_size = len(paths) // N_BATCHES
remainder  = len(paths) % N_BATCHES

batches = []
start = 0
for i in range(N_BATCHES):
    end = start + batch_size + (1 if i < remainder else 0)
    batches.append(paths[start:end])
    start = end

print(f"Batch sizes: {[len(b) for b in batches]}")

TEMPLATE = r'''#!/usr/bin/env python3
"""MM-GBSA batch __BATCH_IDX__: __N_LIGS__ ligands"""
import json
from pathlib import Path
from modulon.governance.toolkit import run_aidd_tool

REC  = "__REC__"
WDIR = "__WDIR__"
LIGS = __LIGS__

results = []
for lig_path in LIGS:
    name = Path(lig_path).stem.replace("_best_pose_H", "")
    try:
        r = run_aidd_tool("gbsa", {
            "task":              "protein-ligand",
            "proteinFile":       REC,
            "ligandFile":        lig_path,
            "mode":              "em",
            "method":            "gb",
            "proteinForceField": "amber99sb-ildn",
            "ligandForceField":  "gaff2",
            "ligandCharge":      "bcc",
            "threads":           4,
        })
        rc = r.get("rc")
        o  = r.get("output", {})
        res_list = o.get("results", [])
        res = res_list[0] if res_list else {}
        row = {
            "ligandName":         name,
            "dG_kcal_mol":        o.get("best_dG_kcal_per_mol"),
            "TOTAL":              float(res.get("TOTAL", 0)) if res else None,
            "Van_der_Waals":      float(res.get("Van der Waals", 0)) if res else None,
            "Electrostatic":      float(res.get("Electrostatic", 0)) if res else None,
            "Polar_Solvation":    float(res.get("Polar Solvation", 0)) if res else None,
            "NonPolar_Solvation": float(res.get("Non-Polar Solvation", 0)) if res else None,
            "Gas":                float(res.get("Gas", 0)) if res else None,
            "Solvation":          float(res.get("Solvation", 0)) if res else None,
            "status":             res.get("status", "F") if res else "F",
            "rc":                 rc,
        }
    except Exception as e:
        row = {"ligandName": name, "dG_kcal_mol": None, "TOTAL": None,
               "status": "F", "rc": -1, "error": str(e)}
    results.append(row)
    dg = row["dG_kcal_mol"]
    if dg is not None:
        print(f"  {name}: dG={dg:.3f} kcal/mol")
    else:
        print(f"  {name}: FAILED rc={row['rc']}")

outfile = f"__WDIR__/gbsa_batch_results___BATCH_IDX_ZPAD__.json"
with open(outfile, "w") as f:
    json.dump(results, f, indent=2)
print(f"Batch __BATCH_IDX__: saved {len(results)} results to " + outfile)
'''

script_dir = WDIR / "gbsa_batches"
script_dir.mkdir(exist_ok=True)

for i, batch in enumerate(batches):
    code = (TEMPLATE
            .replace("__BATCH_IDX__", str(i))
            .replace("__BATCH_IDX_ZPAD__", f"{i:02d}")
            .replace("__N_LIGS__", str(len(batch)))
            .replace("__REC__", REC)
            .replace("__WDIR__", str(WDIR))
            .replace("__LIGS__", json.dumps(batch, indent=4)))
    out = script_dir / f"batch_{i:02d}.py"
    out.write_text(code)
    print(f"  batch_{i:02d}.py: {len(batch)} ligands")

print(f"\nAll {N_BATCHES} batch scripts written to {script_dir}/")
