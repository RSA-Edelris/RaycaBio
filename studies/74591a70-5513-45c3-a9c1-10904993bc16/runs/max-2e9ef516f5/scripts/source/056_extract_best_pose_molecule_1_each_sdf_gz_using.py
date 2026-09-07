
import os, gzip, subprocess
import numpy as np

# ── extract best pose (molecule 1) from each SDF.gz using obabel ─────────────
poses_dir = f"{WORK}/poses"
best_dir   = f"{WORK}/best_poses"
os.makedirs(best_dir, exist_ok=True)

names = sorted([f.replace("_poses.sdf.gz", "") 
                for f in os.listdir(poses_dir) if f.endswith("_poses.sdf.gz")])

extracted = 0
for name in names:
    src = f"{poses_dir}/{name}_poses.sdf.gz"
    dst = f"{best_dir}/{name}_pose1.sdf"
    if os.path.exists(dst):
        extracted += 1
        continue
    # use obabel to extract first molecule only
    result = subprocess.run(
        ["obabel", src, "-O", dst, "-f", "1", "-l", "1"],
        capture_output=True, text=True
    )
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        extracted += 1
    else:
        print(f"  WARN: {name} extraction failed: {result.stderr[:80]}")

print(f"Extracted {extracted}/{len(names)} best poses to {best_dir}")
print("Sample:", os.listdir(best_dir)[:3])
