#!/usr/bin/env python3
"""MM/GBSA — skip sander minimize, run MMPBSA.py directly on tleap rst7 (single-frame)."""
import os, subprocess, json, re

BASE = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'
mmgbsa_dir = os.path.join(BASE, 'mmgbsa')

PYTHON = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/python'
AMBER  = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin'
mmpbsa = os.path.join(AMBER, 'MMPBSA.py')

compounds = [
    'CTX-1020521', 'CTX-1020520', 'CTX-1020810', 'CTX-1019660', 'CTX-1020458',
    'CTX-1019813', 'CTX-1020882', 'CTX-1020555', 'CTX-1020816', 'CTX-1020751',
    'CTX-1017233',
]

MMPBSA_IN = """Input file for running GB
&general
 startframe=1, endframe=1, verbose=2,
/
&gb
 igb=5, saltcon=0.150,
/
"""

AMBERHOME = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
ENV = {**os.environ, 'AMBERHOME': AMBERHOME}

def run(cmd, cwd=None, timeout=600):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=ENV)
    if r.returncode != 0:
        raise RuntimeError(f"{os.path.basename(str(cmd[0]))} rc={r.returncode}\n"
                           f"STDERR: {r.stderr[-2000:]}\nSTDOUT: {r.stdout[-1000:]}")
    return r

results = {}
log = open(os.path.join(BASE, 'mmgbsa_run4.log'), 'w', buffering=1)

for name in compounds:
    log.write(f"\n=== {name} ===\n"); log.flush()
    wdir = os.path.join(mmgbsa_dir, name)

    for f in ['complex.prmtop', 'complex.rst7', 'rec.prmtop', 'lig.prmtop']:
        if not os.path.exists(os.path.join(wdir, f)):
            log.write(f"  MISSING {f}\n"); log.flush()
            results[name] = {'error': f'missing {f}'}
            break
    else:
        with open(os.path.join(wdir, 'mmpbsa.in'), 'w') as f:
            f.write(MMPBSA_IN)

        # Use complex.rst7 directly as single-frame trajectory — no sander minimize
        try:
            r = run([PYTHON, mmpbsa, '-O',
                     '-i',  os.path.join(wdir, 'mmpbsa.in'),
                     '-o',  os.path.join(wdir, 'FINAL_RESULTS_MMGBSA.dat'),
                     '-cp', os.path.join(wdir, 'complex.prmtop'),
                     '-rp', os.path.join(wdir, 'rec.prmtop'),
                     '-lp', os.path.join(wdir, 'lig.prmtop'),
                     '-y',  os.path.join(wdir, 'complex.rst7')],
                    cwd=wdir, timeout=600)
            log.write("  MMPBSA.py done\n"); log.flush()
        except subprocess.TimeoutExpired:
            log.write("  MMPBSA TIMEOUT\n"); log.flush()
            results[name] = {'error': 'mmpbsa timeout'}
            continue
        except Exception as e:
            log.write(f"  MMPBSA FAILED: {e}\n"); log.flush()
            results[name] = {'error': f'mmpbsa: {str(e)[:400]}'}
            continue

        # Parse result
        dat = os.path.join(wdir, 'FINAL_RESULTS_MMGBSA.dat')
        try:
            txt = open(dat).read()
            log.write(f"  last 800 chars of dat:\n{txt[-800:]}\n"); log.flush()
            # MMPBSA.py output: "DELTA Total" or "ΔTOTAL" line
            m = re.search(r'DELTA Total\s+([-\d.]+)', txt, re.IGNORECASE)
            if not m:
                m = re.search(r'DELTA TOTAL\s+([-\d.]+)', txt, re.IGNORECASE)
            if not m:
                for line in txt.split('\n'):
                    if re.search(r'TOTAL', line, re.IGNORECASE) and 'DELTA' in line.upper():
                        nums = re.findall(r'-?\d+\.\d+', line)
                        if nums:
                            dg = float(nums[0])
                            log.write(f"  ΔG_MMGBSA = {dg:.2f} kcal/mol\n"); log.flush()
                            results[name] = {'dg_mmgbsa': dg}
                            m = 'line'
                            break
            if m and m != 'line':
                dg = float(m.group(1))
                log.write(f"  ΔG_MMGBSA = {dg:.2f} kcal/mol\n"); log.flush()
                results[name] = {'dg_mmgbsa': dg}
            elif not m:
                log.write(f"  PARSE FAILED\n"); log.flush()
                results[name] = {'error': 'parse: no DELTA TOTAL'}
        except Exception as e:
            log.write(f"  PARSE FAILED: {e}\n"); log.flush()
            results[name] = {'error': f'parse: {e}'}

with open(os.path.join(mmgbsa_dir, 'mmgbsa_results.json'), 'w') as f:
    json.dump(results, f, indent=2)
log.write("\nALL DONE\n"); log.flush()
log.close()
print("ALL DONE")
