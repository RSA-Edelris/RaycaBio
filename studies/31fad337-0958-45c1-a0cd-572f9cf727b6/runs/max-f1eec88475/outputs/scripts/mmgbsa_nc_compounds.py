#!/usr/bin/env python3
"""
MM-GBSA binding free energies for NC-001 to NC-010.
Same parameters as the 84-compound campaign:
  task=protein-ligand, mode=em, method=gb
  amber99sb-ildn + gaff2 + bcc, receptor_gromacs_ready.pdb
Runs sequentially (one at a time) to avoid acpype concurrency failures.
Saves per-compound results incrementally to nc_mmgbsa_results.json.
"""
import sys, json, time
sys.path.insert(0, "/home/ubuntu/rayca-modulon/src")

from pathlib import Path
from modulon.governance.toolkit import run_aidd_tool
from rdkit import Chem

WDIR    = Path("/home/ubuntu/rayca-sessions/31fad337-0958-45c1-a0cd-572f9cf727b6-0505c6de016f/cdk2_campaign")
REC     = str(WDIR / "receptor_gromacs_ready.pdb")
POSES_H = WDIR / "poses_all_H"
POSES_H.mkdir(exist_ok=True)
RESULTS = WDIR / "nc_mmgbsa_results.json"

NC_NAMES = [f"NC-{i:03d}" for i in range(1, 11)]

# ── Step 1: add explicit H to best poses ────────────────────────────────────
print("=== Step 1: Adding explicit H to NC best poses ===")
for name in NC_NAMES:
    src = WDIR / "poses_all" / f"{name}_best_pose.sdf"
    dst = POSES_H / f"{name}_best_pose_H.sdf"
    if dst.exists():
        print(f"  {name}: H-SDF already exists, skip")
        continue
    if not src.exists():
        print(f"  {name}: WARN — best_pose.sdf missing, cannot add H")
        continue
    suppl = Chem.SDMolSupplier(str(src), removeHs=False, sanitize=True)
    mol = next((m for m in suppl if m is not None), None)
    if mol is None:
        print(f"  {name}: WARN — unreadable SDF")
        continue
    mol_h = Chem.AddHs(mol, addCoords=True)
    w = Chem.SDWriter(str(dst))
    w.write(mol_h)
    w.close()
    nh = sum(1 for a in mol_h.GetAtoms() if a.GetSymbol() == "H")
    print(f"  {name}: {mol.GetNumAtoms()} → {mol_h.GetNumAtoms()} atoms ({nh} H added)")

# ── Step 2: MM-GBSA ─────────────────────────────────────────────────────────
print("\n=== Step 2: MM-GBSA (sequential) ===")

if RESULTS.exists():
    done_map = {r["ligandName"]: r for r in json.loads(RESULTS.read_text())}
else:
    done_map = {}

all_rows = list(done_map.values())

for name in NC_NAMES:
    if name in done_map and done_map[name].get("dG_kcal_mol") is not None:
        print(f"SKIP {name}: already scored (dG={done_map[name]['dG_kcal_mol']:.3f})")
        continue

    lig_path = str(POSES_H / f"{name}_best_pose_H.sdf")
    if not Path(lig_path).exists():
        print(f"SKIP {name}: H-SDF missing")
        all_rows.append({"ligandName": name, "dG_kcal_mol": None, "status": "F",
                         "error": "H-SDF missing"})
        continue

    t0 = time.time()
    try:
        r      = run_aidd_tool("gbsa", {
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
        rc      = r.get("rc")
        o       = r.get("output", {})
        res_lst = o.get("results", [])
        res     = res_lst[0] if res_lst else {}
        row = {
            "ligandName":         name,
            "dG_kcal_mol":        o.get("best_dG_kcal_per_mol"),
            "Van_der_Waals":      float(res.get("Van der Waals", 0))       if res else None,
            "Electrostatic":      float(res.get("Electrostatic", 0))       if res else None,
            "Polar_Solvation":    float(res.get("Polar Solvation", 0))     if res else None,
            "NonPolar_Solvation": float(res.get("Non-Polar Solvation", 0)) if res else None,
            "Gas":                float(res.get("Gas", 0))                 if res else None,
            "Solvation":          float(res.get("Solvation", 0))           if res else None,
            "status":             res.get("status", "F")                   if res else "F",
            "rc":                 rc,
        }
    except Exception as e:
        row = {"ligandName": name, "dG_kcal_mol": None, "status": "F",
               "rc": -1, "error": str(e)}

    dt  = time.time() - t0
    dg  = row["dG_kcal_mol"]
    tag = f"dG={dg:.3f} kcal/mol" if dg is not None else f"FAILED: {row.get('error','?')[:60]}"
    print(f"{name}: {tag}  ({dt:.0f}s)", flush=True)

    # Remove old entry for this name if re-running
    all_rows = [r for r in all_rows if r.get("ligandName") != name]
    all_rows.append(row)
    # Sort by dG ascending (best binder first)
    all_rows.sort(key=lambda x: x["dG_kcal_mol"] if x.get("dG_kcal_mol") is not None else 9999)
    RESULTS.write_text(json.dumps(all_rows, indent=2))

ok   = sum(1 for r in all_rows if r.get("dG_kcal_mol") is not None)
fail = len(all_rows) - ok
print(f"\nDone: {ok}/{len(NC_NAMES)} succeeded, {fail} failed")
if all_rows and all_rows[0].get("dG_kcal_mol") is not None:
    top = all_rows[0]
    print(f"Best: {top['ligandName']}  dG = {top['dG_kcal_mol']:.3f} kcal/mol")
print(f"Results: {RESULTS}")
