#!/usr/bin/env python3
"""Run remaining MM-GBSA calculations with 9 parallel threads.
Saves per-thread JSON after each ligand; merges all at the end.
"""
import json, threading, time
from pathlib import Path
from modulon.governance.toolkit import run_aidd_tool

WDIR = Path("/home/ubuntu/rayca-sessions/31fad337-0958-45c1-a0cd-572f9cf727b6-0505c6de016f/cdk2_campaign")
REC  = str(WDIR / "receptor_gromacs_ready.pdb")

# Load already-completed results (batch_00)
done_file = WDIR / "gbsa_batch_results_00.json"
batch00   = json.loads(done_file.read_text())
done_names = {r["ligandName"] for r in batch00}
print(f"Already done (batch_00): {len(done_names)} ligands")

# Full ligand list minus already done
all_paths = json.loads((WDIR / "gbsa_lig_paths.json").read_text())
remaining  = [p for p in all_paths
              if Path(p).stem.replace("_best_pose_H", "") not in done_names]
print(f"Remaining: {len(remaining)} ligands to score")

# Split into N_THREADS batches
N_THREADS  = 9
chunk      = len(remaining) // N_THREADS
rem        = len(remaining) % N_THREADS
batches    = []
start      = 0
for i in range(N_THREADS):
    end = start + chunk + (1 if i < rem else 0)
    batches.append(remaining[start:end])
    start = end
print(f"Thread sizes: {[len(b) for b in batches]}")

results_lock = threading.Lock()
all_results  = list(batch00)  # seed with already-done

def run_thread(ligs, tid):
    thread_rows = []
    outfile = WDIR / f"gbsa_thread_{tid:02d}.json"
    for j, lig_path in enumerate(ligs):
        name = Path(lig_path).stem.replace("_best_pose_H", "")
        t0 = time.time()
        try:
            r   = run_aidd_tool("gbsa", {
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
                "TOTAL":              float(res.get("TOTAL", 0))             if res else None,
                "Van_der_Waals":      float(res.get("Van der Waals", 0))     if res else None,
                "Electrostatic":      float(res.get("Electrostatic", 0))     if res else None,
                "Polar_Solvation":    float(res.get("Polar Solvation", 0))   if res else None,
                "NonPolar_Solvation": float(res.get("Non-Polar Solvation", 0)) if res else None,
                "Gas":                float(res.get("Gas", 0))               if res else None,
                "Solvation":          float(res.get("Solvation", 0))         if res else None,
                "status":             res.get("status", "F")                 if res else "F",
                "rc":                 rc,
            }
        except Exception as e:
            row = {"ligandName": name, "dG_kcal_mol": None, "TOTAL": None,
                   "status": "F", "rc": -1, "error": str(e)}
        thread_rows.append(row)
        dt  = time.time() - t0
        dg  = row["dG_kcal_mol"]
        tag = f"dG={dg:.2f}" if dg is not None else "FAILED"
        print(f"T{tid} [{j+1}/{len(ligs)}] {name}: {tag}  ({dt:.0f}s)", flush=True)
        outfile.write_text(json.dumps(thread_rows, indent=2))
        with results_lock:
            all_results.append(row)
    print(f"T{tid}: complete ({len(thread_rows)} ligands)", flush=True)

# Launch
t_start = time.time()
threads = [threading.Thread(target=run_thread, args=(b, i), daemon=True)
           for i, b in enumerate(batches)]
for t in threads:
    t.start()
for t in threads:
    t.join(timeout=870)

elapsed = time.time() - t_start
print(f"\nAll threads joined in {elapsed:.0f}s")

# Merge and save final
all_results.sort(key=lambda x: x.get("dG_kcal_mol") if x.get("dG_kcal_mol") is not None else 9999)
outfile = WDIR / "mmgbsa_results.json"
outfile.write_text(json.dumps(all_results, indent=2))
n_ok   = sum(1 for r in all_results if r.get("dG_kcal_mol") is not None)
n_fail = len(all_results) - n_ok
print(f"FINAL: {len(all_results)} total, {n_ok} success, {n_fail} failed")
if all_results and all_results[0].get("dG_kcal_mol") is not None:
    top = all_results[0]
    print(f"Best: {top['ligandName']}  dG = {top['dG_kcal_mol']:.3f} kcal/mol")
