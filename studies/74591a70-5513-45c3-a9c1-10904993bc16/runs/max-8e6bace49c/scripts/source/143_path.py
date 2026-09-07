
import json
from pathlib import Path

BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")

# ── Phase 1 verification ──
enantio_sdf = BASE / "CRBN_ID_enantio_2.sdf"
p1 = {
    "CRBN_ID_enantio_2.sdf exists": enantio_sdf.exists(),
    "CRBN_ID_enantio_2.sdf bytes": enantio_sdf.stat().st_size if enantio_sdf.exists() else 0,
}
if enantio_sdf.exists():
    text = enantio_sdf.read_text(errors='replace')
    n_mols = text.count('$$$$')
    p1["compound count ($$$$)"] = n_mols
    # Check 3D: count lines with non-zero Z
    has_3d = any(
        len(parts := line.split()) >= 3 and abs(float(parts[2])) > 0.01
        for line in text.splitlines()
        if len(line.split()) == 3 and all(s.replace('.','').replace('-','').isdigit() for s in line.split())
    )
    p1["has non-zero Z coords"] = has_3d

# ── Phase 2 verification ──
dock2 = BASE / "docking2_results.json"
best2 = BASE / "best_poses2"
best2_top1 = BASE / "best_poses2_top1"

p2 = {
    "docking2_results.json exists": dock2.exists(),
}
if dock2.exists():
    data = json.loads(dock2.read_text())
    p2["compounds in results"] = len(data)
    affinities = [v['affinity'] for v in data.values() if isinstance(v, dict) and 'affinity' in v]
    if affinities:
        p2["affinity min"] = round(min(affinities), 2)
        p2["affinity max"] = round(max(affinities), 2)

p2["best_poses2/ SDF files"] = len(list(best2.glob("*.sdf"))) if best2.exists() else 0
p2["best_poses2_top1/ SDF files"] = len(list(best2_top1.glob("*.sdf"))) if best2_top1.exists() else 0

# ── Phase 3 verification ──
gbsa_json = BASE / "mmgbsa2_results.json"
fp_json   = BASE / "interaction_fingerprints.json"
annot_sdf = BASE / "CRBN_ID_enantio2_docking_GBSA.sdf"
report_md = BASE / "CRBN_docking_mmgbsa_report.md"

p3 = {
    "mmgbsa2_results.json exists": gbsa_json.exists(),
    "interaction_fingerprints.json exists": fp_json.exists(),
    "CRBN_ID_enantio2_docking_GBSA.sdf exists": annot_sdf.exists(),
    "CRBN_docking_mmgbsa_report.md exists": report_md.exists(),
}
if gbsa_json.exists():
    gbsa_data = json.loads(gbsa_json.read_text())
    p3["MM-GBSA compound count"] = len(gbsa_data)
    dg_vals = [v['dg'] for v in gbsa_data.values() if isinstance(v, dict) and 'dg' in v]
    if dg_vals:
        p3["MMGBSA dG min"] = round(min(dg_vals), 1)
        p3["MMGBSA dG max"] = round(max(dg_vals), 1)
if fp_json.exists():
    fp_data = json.loads(fp_json.read_text())
    p3["interaction fingerprints count"] = len(fp_data.get("fingerprints", {}))
if annot_sdf.exists():
    p3["annotated SDF bytes"] = annot_sdf.stat().st_size
    p3["annotated SDF mol count"] = annot_sdf.read_text(errors='replace').count('$$$$')

print("=== Phase 1 ===")
for k, v in p1.items():
    print(f"  {k}: {v}")
print("\n=== Phase 2 ===")
for k, v in p2.items():
    print(f"  {k}: {v}")
print("\n=== Phase 3 ===")
for k, v in p3.items():
    print(f"  {k}: {v}")
