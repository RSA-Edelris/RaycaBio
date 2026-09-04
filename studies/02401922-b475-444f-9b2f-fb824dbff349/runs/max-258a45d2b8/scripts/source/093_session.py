
import os

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"

# MM/GBSA pipeline script for 11 compounds
# Uses protonated SDF → antechamber AM1-BCC → parmchk2 → tleap → minimize → MMPBSA.py igb=5
# Same methodology as prior session (minimized-pose single-frame)

top11 = [
    ('CTX-1020521', 61, +1),
    ('CTX-1020520', 62, +1),
    ('CTX-1020810', 12, +1),
    ('CTX-1019660', 77, +1),
    ('CTX-1020458', 68, +1),
    ('CTX-1019813', 74, +1),
    ('CTX-1020882',  4, +1),
    ('CTX-1020555', 59, +1),
    ('CTX-1020816', 10, +1),
    ('CTX-1020751', 27,  0),
    ('CTX-1017233', 84, +1),
]

mmgbsa_dir = os.path.join(wd, "mmgbsa")
os.makedirs(mmgbsa_dir, exist_ok=True)

mmpbsa_in = os.path.join(mmgbsa_dir, "mmpbsa.in")
with open(mmpbsa_in, 'w') as f:
    f.write("&general\n  startframe=1, endframe=1, verbose=2,\n/\n&gb\n  igb=5, saltcon=0.150,\n/\n")

min_in = os.path.join(mmgbsa_dir, "min.in")
with open(min_in, 'w') as f:
    f.write("Minimization\n &cntrl\n  imin=1, maxcyc=1500, ncyc=500,\n  ntb=0, igb=5, cut=999.0,\n /\n")

script = f'''#!/usr/bin/env python3
import subprocess, os, re, json

wd = "{wd}"
mmgbsa_dir = "{mmgbsa_dir}"
ligands_dir = os.path.join(wd, "ligands_3d")
antechamber = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/antechamber"
parmchk2    = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/parmchk2"
tleap       = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/tleap"
sander      = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/sander"
mmpbsa_py   = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/MMPBSA.py"
receptor_pdb = os.path.join(wd, "receptor_ab.pdb")

compounds = {top11!r}

results = {{}}

for name, lig_n, nc in compounds:
    print(f"\\n=== {{name}} (lig{{lig_n}}, nc={{nc:+d}}) ===", flush=True)
    cdir = os.path.join(mmgbsa_dir, name)
    os.makedirs(cdir, exist_ok=True)
    sdf_in = os.path.join(ligands_dir, f"lig{{lig_n}}.sdf")

    # Step 1: antechamber AM1-BCC
    mol2_out = os.path.join(cdir, "lig.mol2")
    if not os.path.exists(mol2_out):
        r = subprocess.run([antechamber,
            "-i", sdf_in, "-fi", "sdf",
            "-o", mol2_out, "-fo", "mol2",
            "-c", "bcc", "-s", "2", "-nc", str(nc),
            "-pf", "yes", "-at", "gaff2"],
            capture_output=True, text=True, cwd=cdir, timeout=300)
        print(f"  antechamber RC={{r.returncode}}", flush=True)
        if r.returncode != 0:
            print(f"  STDERR: {{r.stderr[-200:]}}", flush=True)
            results[name] = {{"error": "antechamber"}}
            continue
    else:
        print(f"  antechamber (cached)", flush=True)

    # Step 2: parmchk2
    frcmod = os.path.join(cdir, "lig.frcmod")
    if not os.path.exists(frcmod):
        r = subprocess.run([parmchk2, "-i", mol2_out, "-f", "mol2",
                            "-o", frcmod, "-s", "gaff2"],
            capture_output=True, text=True, cwd=cdir, timeout=60)
        print(f"  parmchk2 RC={{r.returncode}}", flush=True)
    else:
        print(f"  parmchk2 (cached)", flush=True)

    # Step 3: tleap - build dry complex
    tleap_in = os.path.join(cdir, "tleap.in")
    prmtop   = os.path.join(cdir, "complex.prmtop")
    inpcrd   = os.path.join(cdir, "complex.inpcrd")
    lig_prmtop = os.path.join(cdir, "lig.prmtop")
    lig_inpcrd = os.path.join(cdir, "lig.inpcrd")
    rec_prmtop = os.path.join(cdir, "rec.prmtop")
    rec_inpcrd = os.path.join(cdir, "rec.inpcrd")

    with open(tleap_in, 'w') as f:
        f.write(f"""source leaprc.protein.ff14SB
source leaprc.gaff2
source leaprc.water.tip3p
LIG = loadmol2 {{mol2_out}}
loadamberparams {{frcmod}}
saveamberparm LIG {{lig_prmtop}} {{lig_inpcrd}}
REC = loadpdb {{receptor_pdb}}
saveamberparm REC {{rec_prmtop}} {{rec_inpcrd}}
COM = combine {{{{REC LIG}}}}
saveamberparm COM {{prmtop}} {{inpcrd}}
quit
""")
    r = subprocess.run([tleap, "-f", tleap_in],
        capture_output=True, text=True, cwd=cdir, timeout=120)
    print(f"  tleap RC={{r.returncode}}", flush=True)
    if not os.path.exists(prmtop):
        print(f"  tleap FAILED: {{r.stderr[-300:]}}", flush=True)
        results[name] = {{"error": "tleap"}}
        continue

    # Step 4: minimize
    rst_out = os.path.join(cdir, "min.rst7")
    min_out = os.path.join(cdir, "min.out")
    if not os.path.exists(rst_out):
        r = subprocess.run([sander,
            "-O", "-i", "{min_in}", "-o", min_out,
            "-p", prmtop, "-c", inpcrd, "-r", rst_out],
            capture_output=True, text=True, cwd=cdir, timeout=300)
        print(f"  sander minimize RC={{r.returncode}}", flush=True)
    else:
        print(f"  minimize (cached)", flush=True)

    if not os.path.exists(rst_out):
        results[name] = {{"error": "minimize"}}
        continue

    # Step 5: MMPBSA.py single-frame on minimized structure
    mmgbsa_out = os.path.join(cdir, "FINAL_RESULTS_MMGBSA.dat")
    r = subprocess.run([mmpbsa_py,
        "-O", "-i", "{mmpbsa_in}",
        "-cp", prmtop, "-rp", rec_prmtop, "-lp", lig_prmtop,
        "-y", rst_out, "-o", mmgbsa_out],
        capture_output=True, text=True, cwd=cdir, timeout=120)
    print(f"  MMPBSA.py RC={{r.returncode}}", flush=True)

    # Parse result
    dg = None
    if os.path.exists(mmgbsa_out):
        with open(mmgbsa_out) as f:
            for line in f:
                m = re.search(r'DELTA TOTAL\\s+([-\\d.]+)', line)
                if m:
                    dg = float(m.group(1))
                    break
    print(f"  ΔG_bind = {{dg}} kcal/mol", flush=True)
    results[name] = {{"dg_mmgbsa": dg, "nc": nc}}

# Save
import json
with open(os.path.join(mmgbsa_dir, "mmgbsa_results.json"), "w") as f:
    json.dump(results, f, indent=2)
print("\\nALL DONE", flush=True)
print(json.dumps(results, indent=2))
'''

script_path = os.path.join(wd, "run_mmgbsa.py")
with open(script_path, 'w') as f:
    f.write(script)
print(f"Script written: {script_path}")
print(f"MMGBSA dir: {mmgbsa_dir}")
