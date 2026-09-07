#!/usr/bin/env python3
"""Single-frame MM-GBSA endpoint scoring for 22 docked CRBN poses (igb=5, GAFF2/ff14SB)."""

import os, json, re, subprocess, sys
from pathlib import Path

AMBER_BIN   = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin"
VENV_PYTHON = "/home/ubuntu/rayca-runtime/.venv/bin/python3"
BASE        = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
BEST_DIR    = BASE / "best_poses2_top1"
REC_PDB     = BASE / "mmgbsa2" / "receptor_amber.pdb"  # HIS→HID/HIE fixed, H1 N-term
MMGBSA_DIR  = BASE / "mmgbsa2"
RESULTS_FILE= BASE / "mmgbsa2_results.json"

ENV = os.environ.copy()
ENV['PATH'] = AMBER_BIN + ':' + ENV.get('PATH', '')
ENV['AMBERHOME'] = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'

def run(cmd, cwd=None, timeout=300):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                       cwd=cwd, env=ENV, timeout=timeout)
    return r.returncode, r.stdout, r.stderr

def get_net_charge(sdf_path):
    code = (
        "from rdkit import Chem; from rdkit.Chem import rdmolops; "
        f"m=Chem.SDMolSupplier('{sdf_path}',sanitize=True,removeHs=False)[0]; "
        "print(rdmolops.GetFormalCharge(m) if m else 0)"
    )
    r = subprocess.run([VENV_PYTHON, '-c', code], capture_output=True, text=True, timeout=30)
    try:
        return int(r.stdout.strip())
    except Exception:
        return 0

MMPBSA_IN = """\
MM-GBSA endpoint scoring igb5
&general
  endframe=1, verbose=2, keep_files=0,
/
&gb
  igb=5, saltcon=0.100,
/
"""

TLEAP_REC = """\
source leaprc.protein.ff14SB
rec = loadpdb {rec_pdb}
saveamberparm rec {rec_prmtop} {rec_inpcrd}
quit
"""

TLEAP_COM = """\
source leaprc.protein.ff14SB
source leaprc.gaff2
loadamberparams {lig_frcmod}
lig = loadmol2 {lig_mol2}
rec = loadpdb {rec_pdb}
com = combine {{rec lig}}
saveamberparm com {com_prmtop} {com_inpcrd}
saveamberparm rec {rec_prmtop2} {rec_inpcrd2}
saveamberparm lig {lig_prmtop} {lig_inpcrd}
quit
"""

CPPTRAJ_IN = """\
parm {prmtop}
trajin {inpcrd}
trajout {nc_out} netcdf
run
quit
"""

def parse_mmpbsa(dat_text):
    result = {}
    for term in ['DELTA TOTAL', 'VDWAALS', 'EEL', 'EGB', 'ESURF']:
        m = re.search(r'%s\s+([-\d.]+)\s+([-\d.]+)' % re.escape(term), dat_text)
        if m:
            key = term.replace(' ', '_')
            result[key] = float(m.group(1))
            result[key + '_std'] = float(m.group(2))
    return result

def main():
    MMGBSA_DIR.mkdir(exist_ok=True)
    results = json.loads(RESULTS_FILE.read_text()) if RESULTS_FILE.exists() else {}

    # --- Prepare receptor (strip ZN HETATM, keep only ATOM) ---
    rec_stripped = MMGBSA_DIR / "receptor_protein.pdb"
    if not rec_stripped.exists():
        lines = REC_PDB.read_text().splitlines()
        kept = [l for l in lines if l.startswith(('ATOM', 'TER', 'END'))]
        rec_stripped.write_text('\n'.join(kept) + '\n')
        print(f"Receptor stripped: {sum(1 for l in kept if l.startswith('ATOM'))} ATOM records", flush=True)

    # --- Build receptor topology once ---
    rec_prmtop = MMGBSA_DIR / "receptor.prmtop"
    rec_inpcrd  = MMGBSA_DIR / "receptor.inpcrd"
    if not rec_prmtop.exists():
        tl = TLEAP_REC.format(
            rec_pdb=str(rec_stripped),
            rec_prmtop=str(rec_prmtop),
            rec_inpcrd=str(rec_inpcrd),
        )
        tf = MMGBSA_DIR / "tleap_rec.in"
        tf.write_text(tl)
        rc, out, err = run(f"tleap -f {tf}", cwd=MMGBSA_DIR)
        if not rec_prmtop.exists():
            print(f"FATAL: receptor tleap failed\n{err[:600]}", flush=True)
            sys.exit(1)
        print(f"Receptor topology: {rec_prmtop.stat().st_size//1024} KB", flush=True)

    # --- Per-ligand pipeline ---
    names = sorted([f.stem.replace('_pose1', '') for f in BEST_DIR.glob('*_pose1.sdf')])
    print(f"\nProcessing {len(names)} compounds...", flush=True)

    for name in names:
        if name in results and results[name].get('DELTA_TOTAL') is not None:
            print(f"  {name}: skip ({results[name]['DELTA_TOTAL']:.1f})", flush=True)
            continue

        sdf = BEST_DIR / f"{name}_pose1.sdf"
        wd  = MMGBSA_DIR / name
        wd.mkdir(exist_ok=True)
        print(f"  {name}...", flush=True, end=' ')

        nc = get_net_charge(str(sdf))

        # antechamber: Gasteiger charges (fast; AM1BCC times out on 30-38 HA compounds)
        mol2 = wd / "lig.mol2"
        rc, out, err = run(
            f"antechamber -i {sdf} -fi sdf -o {mol2} -fo mol2 "
            f"-c gas -nc {nc} -at gaff2 -rn LIG -dr no",
            cwd=wd, timeout=60
        )
        if not mol2.exists():
            print(f"antechamber FAILED", flush=True)
            results[name] = {'error': f'antechamber: {err[:200]}'}
            RESULTS_FILE.write_text(json.dumps(results, indent=2))
            continue

        # parmchk2
        frcmod = wd / "lig.frcmod"
        run(f"parmchk2 -i {mol2} -f mol2 -o {frcmod}", cwd=wd)

        # tleap complex
        com_prmtop  = wd / "complex.prmtop"
        com_inpcrd  = wd / "complex.inpcrd"
        lig_prmtop  = wd / "ligand.prmtop"
        lig_inpcrd  = wd / "ligand.inpcrd"
        rec_prmtop2 = wd / "receptor.prmtop"
        rec_inpcrd2 = wd / "receptor.inpcrd"

        tl = TLEAP_COM.format(
            lig_frcmod=str(frcmod), lig_mol2=str(mol2),
            rec_pdb=str(rec_stripped),
            com_prmtop=str(com_prmtop), com_inpcrd=str(com_inpcrd),
            rec_prmtop2=str(rec_prmtop2), rec_inpcrd2=str(rec_inpcrd2),
            lig_prmtop=str(lig_prmtop), lig_inpcrd=str(lig_inpcrd),
        )
        tf = wd / "tleap.in"
        tf.write_text(tl)
        rc, out, err = run(f"tleap -f {tf}", cwd=wd, timeout=120)
        if not com_prmtop.exists():
            print(f"tleap FAILED", flush=True)
            results[name] = {'error': f'tleap: {err[:200]}'}
            RESULTS_FILE.write_text(json.dumps(results, indent=2))
            continue

        # cpptraj: inpcrd → netcdf 1-frame trajectory
        com_nc = wd / "complex.nc"
        cp_in  = wd / "cpptraj.in"
        cp_in.write_text(CPPTRAJ_IN.format(
            prmtop=str(com_prmtop), inpcrd=str(com_inpcrd), nc_out=str(com_nc)
        ))
        rc, out, err = run(f"cpptraj -i {cp_in}", cwd=wd)
        if not com_nc.exists():
            print(f"cpptraj FAILED", flush=True)
            results[name] = {'error': f'cpptraj: {err[:200]}'}
            RESULTS_FILE.write_text(json.dumps(results, indent=2))
            continue

        # MMPBSA.py
        mm_in  = wd / "mmpbsa.in"
        mm_out = wd / "FINAL_RESULTS_MMPBSA.dat"
        mm_in.write_text(MMPBSA_IN)
        rc, out, err = run(
            f"MMPBSA.py -O -i {mm_in} "
            f"-cp {com_prmtop} -rp {rec_prmtop2} -lp {lig_prmtop} "
            f"-y {com_nc} -o {mm_out}",
            cwd=wd, timeout=180
        )
        if mm_out.exists():
            parsed = parse_mmpbsa(mm_out.read_text())
            results[name] = parsed
            dg = parsed.get('DELTA_TOTAL', None)
            print(f"ΔG={dg:.1f} kcal/mol" if dg is not None else "parse error", flush=True)
        else:
            results[name] = {'error': f'MMPBSA.py failed rc={rc}: {err[:200]}'}
            print(f"MMPBSA FAILED rc={rc}", flush=True)

        RESULTS_FILE.write_text(json.dumps(results, indent=2))

    # Summary
    print("\n=== MM-GBSA COMPLETE ===", flush=True)
    done = sum(1 for v in results.values() if isinstance(v.get('DELTA_TOTAL'), float))
    print(f"{done}/{len(names)} succeeded", flush=True)
    rows = sorted(
        [(n, v['DELTA_TOTAL']) for n, v in results.items() if isinstance(v.get('DELTA_TOTAL'), float)],
        key=lambda x: x[1]
    )
    print(f"\n{'Name':<25} {'ΔG_GBSA (kcal/mol)':>20}")
    print("─" * 47)
    for n, dg in rows:
        print(f"{n:<25} {dg:>20.2f}")

if __name__ == '__main__':
    main()
