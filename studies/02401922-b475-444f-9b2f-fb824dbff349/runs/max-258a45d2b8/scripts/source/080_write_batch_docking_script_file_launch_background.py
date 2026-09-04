
# Write the batch docking script to a file, then launch as background process

script_content = '''#!/usr/bin/env python3
import subprocess, os, re, time, json

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
ligands_dir = os.path.join(wd, "ligands_3d")
results_dir = os.path.join(wd, "docking_results")
os.makedirs(results_dir, exist_ok=True)

vina_bin = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/vina"
receptor_pdbqt = os.path.join(wd, "receptor.pdbqt")

def sdf_num(f):
    m = re.search(r\'lig(\\d+)\\.sdf\', f)
    return int(m.group(1)) if m else 0

sdf_files = sorted([f for f in os.listdir(ligands_dir) if f.endswith(\'.sdf\')], key=sdf_num)

results = []
t0 = time.time()

for i, sdf_file in enumerate(sdf_files):
    sdf_path = os.path.join(ligands_dir, sdf_file)
    stem = sdf_file.replace(\'.sdf\', \'\')
    pdbqt_path = os.path.join(ligands_dir, stem + \'.pdbqt\')
    out_pdbqt = os.path.join(results_dir, stem + \'_out.pdbqt\')
    log_path = os.path.join(results_dir, stem + \'.log\')

    # Get compound name
    with open(sdf_path) as f:
        name = f.readline().strip()

    # Convert SDF -> PDBQT
    r = subprocess.run(
        [\'/usr/bin/obabel\', sdf_path, \'-O\', pdbqt_path,
         \'--partialcharge\', \'gasteiger\', \'-h\'],
        capture_output=True, text=True
    )
    if r.returncode != 0 or not os.path.exists(pdbqt_path):
        print(f"[{i+1}/84] {name}: PDBQT conversion FAILED")
        results.append({\'name\': name, \'idx\': i+1, \'error\': \'pdbqt_fail\'})
        continue

    # Run vina
    r2 = subprocess.run([
        vina_bin,
        \'--receptor\', receptor_pdbqt,
        \'--ligand\', pdbqt_path,
        \'--out\', out_pdbqt,
        \'--log\', log_path,
        \'--center_x\', \'30.0\',
        \'--center_y\', \'3.4\',
        \'--center_z\', \'-24.8\',
        \'--size_x\', \'25\',
        \'--size_y\', \'25\',
        \'--size_z\', \'25\',
        \'--exhaustiveness\', \'8\',
        \'--num_modes\', \'5\',
        \'--energy_range\', \'3\'
    ], capture_output=True, text=True)

    # Parse scores from log
    scores = re.findall(r\'\\s+(\\d+)\\s+(-[\\d.]+)\\s+[\\d.]+\\s+[\\d.]+\', r2.stdout + r2.stderr)
    if not scores:
        # Try log file
        if os.path.exists(log_path):
            with open(log_path) as lf:
                scores = re.findall(r\'\\s+(\\d+)\\s+(-[\\d.]+)\\s+[\\d.]+\\s+[\\d.]+\', lf.read())
    
    pose_scores = [(int(p), float(s)) for p, s in scores]
    best = pose_scores[0][1] if pose_scores else None
    elapsed = time.time() - t0
    print(f"[{i+1:3d}/84] {name:30s}  best={best}  poses={len(pose_scores)}  t={elapsed:.0f}s", flush=True)
    results.append({\'name\': name, \'idx\': i+1, \'sdf\': sdf_file, \'best_score\': best, \'all_scores\': pose_scores})

# Save JSON summary
out_json = os.path.join(wd, "docking_scores.json")
with open(out_json, \'w\') as f:
    json.dump(results, f, indent=2)

print(f"\\nDone. {len(results)} compounds. Results: {out_json}")
print(f"Total time: {time.time()-t0:.0f}s")
'''

script_path = os.path.join(wd, "run_docking.py")
with open(script_path, 'w') as f:
    f.write(script_content)

# Make executable and launch in background
import subprocess, os
wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
log_out = os.path.join(wd, "docking_batch.log")

proc = subprocess.Popen(
    ['/usr/bin/python3', script_path],
    stdout=open(log_out, 'w'),
    stderr=subprocess.STDOUT,
    cwd=wd
)
print(f"Launched PID {proc.pid}, log: {log_out}")
print("Waiting 15s to confirm startup...")
import time; time.sleep(15)

# Check first few lines
with open(log_out) as f:
    print(f.read())
