#!/usr/bin/env python3
"""MM/GBSA step 2 only: sander minimize + MMPBSA.py on pre-built prmtop/rst7 files."""
import os, subprocess, json, re

BASE = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'
mmgbsa_dir = os.path.join(BASE, 'mmgbsa')

AMBER = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin'
sander = os.path.join(AMBER, 'sander')
mmpbsa = os.path.join(AMBER, 'MMPBSA.py')
PYTHON = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/python'

compounds = [
    'CTX-1020521', 'CTX-1020520', 'CTX-1020810', 'CTX-1019660', 'CTX-1020458',
    'CTX-1019813', 'CTX-1020882', 'CTX-1020555', 'CTX-1020816', 'CTX-1020751',
    'CTX-1017233',
]

MIN_IN = """Minimization
&cntrl
 imin=1, maxcyc=300, ncyc=100,
 ntb=0, igb=5, cut=12.0,
/
"""

MMPBSA_IN = """Input file for running GB
&general
 startframe=1, endframe=1, verbose=2,
/
&gb
 igb=5, saltcon=0.150,
/
"""

def run(cmd, cwd=None, timeout=600):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"{os.path.basename(cmd[0])} rc={r.returncode}\nSTDERR: {r.stderr[-2000:]}\nSTDOUT: {r.stdout[-1000:]}")
    return r

results = {}
log = open(os.path.join(BASE, 'mmgbsa_run3.log'), 'w', buffering=1)

for name in compounds:
    log.write(f"\n=== {name} ===\n"); log.flush()
    wdir = os.path.join(mmgbsa_dir, name)

    # Verify tleap outputs exist
    for f in ['complex.prmtop', 'complex.rst7', 'rec.prmtop', 'lig.prmtop']:
        if not os.path.exists(os.path.join(wdir, f)):
            log.write(f"  MISSING {f} — skipping\n"); log.flush()
            results[name] = {'error': f'missing {f}'}
            break
    else:
        # Write input files fresh
        with open(os.path.join(wdir, 'min.in'), 'w') as f:
            f.write(MIN_IN)
        with open(os.path.join(wdir, 'mmpbsa.in'), 'w') as f:
            f.write(MMPBSA_IN)

        # Sander minimize
        try:
            run([sander, '-O',
                 '-i',   os.path.join(wdir, 'min.in'),
                 '-o',   os.path.join(wdir, 'min.out'),
                 '-p',   os.path.join(wdir, 'complex.prmtop'),
                 '-c',   os.path.join(wdir, 'complex.rst7'),
                 '-r',   os.path.join(wdir, 'min.rst7'),
                 '-ref', os.path.join(wdir, 'complex.rst7')],
                cwd=wdir, timeout=180)
            log.write("  sander done\n"); log.flush()
        except Exception as e:
            log.write(f"  SANDER FAILED: {e}\n"); log.flush()
            results[name] = {'error': f'sander: {str(e)[:300]}'}
            continue

        # MMPBSA.py
        try:
            run([PYTHON, mmpbsa, '-O',
                 '-i',  os.path.join(wdir, 'mmpbsa.in'),
                 '-o',  os.path.join(wdir, 'FINAL_RESULTS_MMGBSA.dat'),
                 '-cp', os.path.join(wdir, 'complex.prmtop'),
                 '-rp', os.path.join(wdir, 'rec.prmtop'),
                 '-lp', os.path.join(wdir, 'lig.prmtop'),
                 '-y',  os.path.join(wdir, 'min.rst7')],
                cwd=wdir, timeout=300)
            log.write("  MMPBSA.py done\n"); log.flush()
        except Exception as e:
            log.write(f"  MMPBSA FAILED: {e}\n"); log.flush()
            results[name] = {'error': f'mmpbsa: {str(e)[:300]}'}
            continue

        # Parse result
        dat = os.path.join(wdir, 'FINAL_RESULTS_MMGBSA.dat')
        try:
            txt = open(dat).read()
            # Try multiple patterns
            m = re.search(r'DELTA Total\s+([-\d.]+)\s+\+/-\s+([-\d.]+)', txt)
            if not m:
                m = re.search(r'DELTA TOTAL\s+([-\d.]+)', txt, re.IGNORECASE)
            if not m:
                # scan lines for the TOTAL delta line
                for line in txt.split('\n'):
                    if re.search(r'TOTAL', line, re.IGNORECASE) and re.search(r'[-\d]', line):
                        nums = re.findall(r'-?\d+\.\d+', line)
                        if nums:
                            dg = float(nums[0])
                            log.write(f"  ΔG_MMGBSA = {dg:.2f} kcal/mol (line-scan)\n"); log.flush()
                            results[name] = {'dg_mmgbsa': dg}
                            m = 'found'
                            break
            if m and m != 'found':
                dg = float(m.group(1))
                log.write(f"  ΔG_MMGBSA = {dg:.2f} kcal/mol\n"); log.flush()
                results[name] = {'dg_mmgbsa': dg}
            elif m != 'found':
                log.write(f"  PARSE FAILED: no DELTA TOTAL in output\n  Last 500 chars: {txt[-500:]}\n"); log.flush()
                results[name] = {'error': 'parse: no DELTA TOTAL'}
        except Exception as e:
            log.write(f"  PARSE FAILED: {e}\n"); log.flush()
            results[name] = {'error': f'parse: {e}'}

with open(os.path.join(mmgbsa_dir, 'mmgbsa_results.json'), 'w') as f:
    json.dump(results, f, indent=2)
log.write("\nALL DONE\n"); log.flush()
log.close()
print("ALL DONE")
