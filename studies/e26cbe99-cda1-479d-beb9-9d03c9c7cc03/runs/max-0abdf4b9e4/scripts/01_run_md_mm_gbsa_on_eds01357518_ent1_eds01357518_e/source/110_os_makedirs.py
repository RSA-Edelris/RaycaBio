
import os, subprocess
from rdkit import Chem
from rdkit.Chem import AllChem

WD       = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'
AMBERHOME= '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
PY3      = f'{AMBERHOME}/bin/python3'
REC_PDB  = f'{WD}/md_EDS01806218_ent2/receptor_tleap.pdb'   # reuse prepared receptor
env      = {**os.environ, 'AMBERHOME': AMBERHOME}

COMPOUNDS = ['EDS01357518_ent1', 'EDS01357518_ent2', 'EDS01806218_ent1', 'EDS01889984']

EM_MDP = """\
; Energy minimisation
integrator      = steep
nsteps          = 10000
emtol           = 100.0
emstep          = 0.01
nstlist         = 10
cutoff-scheme   = Verlet
ns_type         = grid
coulombtype     = PME
rcoulomb        = 1.0
rvdw            = 1.0
pbc             = xyz
DispCorr        = EnerPres
"""

NPT_EQ_MDP = """\
; NPT equilibration 200 ps
integrator      = md
nsteps          = 100000
dt              = 0.002
nstxout         = 5000
nstvout         = 5000
nstenergy       = 5000
nstlog          = 5000
cutoff-scheme   = Verlet
ns_type         = grid
nstlist         = 10
coulombtype     = PME
rcoulomb        = 1.0
rvdw            = 1.0
pbc             = xyz
DispCorr        = EnerPres
tcoupl          = V-rescale
tc-grps         = Protein_LIG Water_and_ions
tau_t           = 0.1   0.1
ref_t           = 300   300
pcoupl          = Berendsen
pcoupltype      = isotropic
tau_p           = 2.0
ref_p           = 1.0
compressibility = 4.5e-5
constraints     = h-bonds
constraint_algorithm = LINCS
lincs_iter      = 1
lincs_order     = 4
gen_vel         = yes
gen_temp        = 300
gen_seed        = 42
"""

PROD_MDP = """\
; 10 ns NPT production
integrator      = md
nsteps          = 5000000
dt              = 0.002
nstxout-compressed = 5000
nstvout         = 0
nstenergy       = 5000
nstlog          = 5000
cutoff-scheme   = Verlet
ns_type         = grid
nstlist         = 10
coulombtype     = PME
rcoulomb        = 1.0
rvdw            = 1.0
pbc             = xyz
DispCorr        = EnerPres
tcoupl          = V-rescale
tc-grps         = Protein_LIG Water_and_ions
tau_t           = 0.1   0.1
ref_t           = 300   300
pcoupl          = Parrinello-Rahman
pcoupltype      = isotropic
tau_p           = 2.0
ref_p           = 1.0
compressibility = 4.5e-5
constraints     = h-bonds
constraint_algorithm = LINCS
lincs_iter      = 1
lincs_order     = 4
gen_vel         = no
continuation    = yes
"""

MMPBSA_IN = """\
Per-residue MM-GBSA for CRBN pocket
&general
  startframe = 200,
  endframe   = 1000,
  interval   = 4,
  verbose    = 2,
  keep_files = 0,
/
&gb
  igb     = 5,
  saltcon = 0.15,
/
"""

results = {}

for cid in COMPOUNDS:
    d = f'{WD}/md_{cid}'
    os.makedirs(d, exist_ok=True)
    print(f"\n{'='*60}")
    print(f"  {cid}")
    print(f"{'='*60}")

    # ── 1. Extract best pose (pose 0) and add explicit H ───────────────
    with open(f'{WD}/poses_{cid}.sdf') as fh:
        blocks = [b.strip() for b in fh.read().split('$$$$') if b.strip()]
    mol = Chem.MolFromMolBlock(blocks[0], removeHs=False)
    mol_h = AllChem.AddHs(mol, addCoords=True)
    nc = sum(a.GetFormalCharge() for a in mol_h.GetAtoms())
    print(f"  Atoms: {mol_h.GetNumAtoms()}, net charge: {nc}")
    with Chem.SDWriter(f'{d}/ligand_h.sdf') as w:
        w.write(mol_h)
    results[cid] = {'nc': nc}

    # ── 2. antechamber: GAFF2 + AM1-BCC ───────────────────────────────
    r = subprocess.run([
        'antechamber',
        '-i', f'{d}/ligand_h.sdf', '-fi', 'sdf',
        '-o', f'{d}/ligand.mol2', '-fo', 'mol2',
        '-c', 'bcc', '-nc', str(nc), '-rn', 'LIG', '-at', 'gaff2', '-pf', 'y'
    ], capture_output=True, text=True, cwd=d, env=env)
    mol2_ok = os.path.exists(f'{d}/ligand.mol2') and os.path.getsize(f'{d}/ligand.mol2') > 100
    print(f"  antechamber: {'OK' if mol2_ok else 'FAIL'} ({os.path.getsize(d+'/ligand.mol2') if mol2_ok else 'missing'} B)")
    if not mol2_ok:
        print("  STDERR:", r.stderr[-400:])
        continue

    # ── 3. parmchk2: missing GAFF2 parameters ─────────────────────────
    r = subprocess.run([
        'parmchk2', '-i', f'{d}/ligand.mol2', '-f', 'mol2',
        '-o', f'{d}/ligand.frcmod', '-s', 'gaff2'
    ], capture_output=True, text=True, cwd=d, env=env)
    frcmod_ok = os.path.exists(f'{d}/ligand.frcmod')
    print(f"  parmchk2:    {'OK' if frcmod_ok else 'FAIL'}")

    # ── 4. tleap: solvated AMBER topology ─────────────────────────────
    tleap_in = f"""\
source leaprc.protein.ff14SB
source leaprc.gaff2
source leaprc.water.tip3p

LIG = loadmol2 {d}/ligand.mol2
loadamberparams {d}/ligand.frcmod

REC = loadpdb {REC_PDB}
complex = combine {{ REC LIG }}

check complex

solvateBox complex TIP3PBOX 12.0
addIons complex Na+ 0
addIons complex Cl- 0
addIons2 complex Na+ 0.15

savepdb complex {d}/complex_solvated.pdb
saveamberparm complex {d}/complex.prmtop {d}/complex.inpcrd

quit
"""
    with open(f'{d}/tleap.in', 'w') as fh:
        fh.write(tleap_in)
    r = subprocess.run(['tleap', '-f', f'{d}/tleap.in'],
                       capture_output=True, text=True, cwd=d, env=env)
    prmtop_ok = os.path.exists(f'{d}/complex.prmtop') and os.path.getsize(f'{d}/complex.prmtop') > 10000
    if prmtop_ok:
        sz_prmtop = os.path.getsize(f'{d}/complex.prmtop')
        print(f"  tleap:       OK ({sz_prmtop:,} B)")
        # extract atom count from leap.log
        for line in (r.stdout+r.stderr).splitlines():
            if 'Total atoms' in line or 'added' in line.lower() or 'Added' in line:
                print(f"    {line.strip()}")
    else:
        print(f"  tleap:       FAIL")
        print("  stderr tail:", (r.stdout+r.stderr)[-600:])
        continue

    # ── 5. parmed: AMBER → GROMACS ────────────────────────────────────
    pmd_script = f"""\
import parmed as pmd
amber_sys = pmd.load_file("{d}/complex.prmtop", "{d}/complex.inpcrd")
n = len(amber_sys.atoms); r = len(amber_sys.residues); b = amber_sys.box
print(f"atoms={{n}} residues={{r}} box={{b[0]:.2f}}x{{b[1]:.2f}}x{{b[2]:.2f}}")
amber_sys.save("{d}/complex.top", overwrite=True)
amber_sys.save("{d}/complex.gro", overwrite=True)
print("DONE")
"""
    with open(f'{d}/run_parmed.py', 'w') as fh:
        fh.write(pmd_script)
    r = subprocess.run([PY3, f'{d}/run_parmed.py'],
                       capture_output=True, text=True, cwd=d)
    gro_ok = os.path.exists(f'{d}/complex.gro') and os.path.getsize(f'{d}/complex.gro') > 10000
    print(f"  parmed:      {'OK' if gro_ok else 'FAIL'}", r.stdout.strip() if gro_ok else r.stderr[-200:])

    # ── 6. GROMACS index ───────────────────────────────────────────────
    # First get group numbers for LIG
    r_ndx = subprocess.run(
        ['gmx', 'make_ndx', '-f', f'{d}/complex.gro', '-o', f'{d}/index_tmp.ndx'],
        input='q\n', capture_output=True, text=True, env=env
    )
    # Find Protein and LIG group numbers
    groups = {}
    for line in (r_ndx.stdout + r_ndx.stderr).splitlines():
        if line.strip() and line.strip()[0].isdigit():
            parts = line.strip().split()
            if len(parts) >= 3:
                groups[parts[2]] = parts[0]

    prot_g = groups.get('Protein', '1')
    lig_g  = groups.get('LIG', None)
    if lig_g is None:
        # scan for LIG
        for k, v in groups.items():
            if 'LIG' in k:
                lig_g = v
                break
    print(f"  Groups: Protein={prot_g}, LIG={lig_g}")

    # Build index: Protein_LIG and Water_and_ions
    # We need to find the water/ion groups too
    wat_g = groups.get('Water_and_ions', groups.get('SOL', groups.get('Water', None)))
    if wat_g is None:
        for k, v in groups.items():
            if 'Water' in k or 'SOL' in k or 'Ion' in k:
                wat_g = v
                break

    ndx_cmds = f"{prot_g} | {lig_g}\nname {int(max(groups.values(), key=int))+1} Protein_LIG\n"
    # find what's left
    r2 = subprocess.run(
        ['gmx', 'make_ndx', '-f', f'{d}/complex.gro', '-o', f'{d}/index.ndx'],
        input=ndx_cmds + 'q\n',
        capture_output=True, text=True, env=env
    )
    ndx_ok = os.path.exists(f'{d}/index.ndx')
    print(f"  make_ndx:    {'OK' if ndx_ok else 'FAIL'}")

    # ── 7. MDP files ──────────────────────────────────────────────────
    for fname, content in [('em.mdp', EM_MDP), ('npt_eq.mdp', NPT_EQ_MDP), ('prod.mdp', PROD_MDP)]:
        with open(f'{d}/{fname}', 'w') as fh:
            fh.write(content)

    # ── 8. grompp EM (validate topology) ──────────────────────────────
    r = subprocess.run([
        'gmx', 'grompp', '-f', f'{d}/em.mdp', '-c', f'{d}/complex.gro',
        '-p', f'{d}/complex.top', '-n', f'{d}/index.ndx',
        '-o', f'{d}/em.tpr', '-maxwarn', '5'
    ], capture_output=True, text=True, env=env)
    tpr_ok = os.path.exists(f'{d}/em.tpr') and os.path.getsize(f'{d}/em.tpr') > 10000
    print(f"  grompp EM:   {'OK' if tpr_ok else 'FAIL'}")
    if not tpr_ok:
        print("  ", (r.stdout+r.stderr)[-400:])

    # ── 9. ante-MMPBSA.py: stripped topologies ────────────────────────
    mmpbsa_in_file = f'{d}/mmpbsa.in'
    with open(mmpbsa_in_file, 'w') as fh:
        fh.write(MMPBSA_IN)

    r = subprocess.run([
        'ante-MMPBSA.py',
        '-p', f'{d}/complex.prmtop',
        '-c', f'{d}/complex_nowater.prmtop',
        '-r', f'{d}/receptor.prmtop',
        '-l', f'{d}/ligand.prmtop',
        '-s', ':WAT,Cl-',
        '-n', ':LIG',
        '--radii', 'mbondi2',
    ], capture_output=True, text=True, cwd=d, env=env)
    ante_ok = all(os.path.exists(f'{d}/{f}')
                  for f in ['complex_nowater.prmtop', 'receptor.prmtop', 'ligand.prmtop'])
    print(f"  ante-MMPBSA: {'OK' if ante_ok else 'FAIL'}")
    if not ante_ok:
        print("  ", r.stderr[-300:])

    results[cid]['ready'] = tpr_ok and ante_ok

print("\n\n=== Summary ===")
for cid, v in results.items():
    print(f"  {cid}: ready={v.get('ready', False)}")
