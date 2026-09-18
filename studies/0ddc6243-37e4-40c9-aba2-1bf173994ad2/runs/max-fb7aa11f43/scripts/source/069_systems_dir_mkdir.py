
import subprocess, pathlib

SYSTEMS_DIR = SESSION / "md" / "systems"
SYSTEMS_DIR.mkdir(parents=True, exist_ok=True)
RECEPTOR = SESSION / "md" / "receptor_nozn.pdb"

print("Building AMBER systems with tleap...")
results = {}
for lig in LIGS:
    d     = SYSTEMS_DIR / lig
    d.mkdir(exist_ok=True)
    mol2  = PARAM_DIR / lig / f"{lig}_fixed.mol2"
    frcmod = PARAM_DIR / lig / f"{lig}.frcmod"

    tleap_in = d / "tleap.in"
    tleap_in.write_text(f"""source leaprc.protein.ff14SB
source leaprc.gaff2
source leaprc.water.tip3p
loadamberparams frcmod.ionsjc_tip3p
loadamberparams {frcmod}
LIG_MOL = loadmol2 {mol2}
PROT = loadpdb {RECEPTOR}
MOL = combine {{PROT LIG_MOL}}
solvateOct MOL TIP3PBOX 12.0
addIons MOL Na+ 0
addIons MOL Na+ 50 Cl- 50
charge MOL
saveamberparm MOL {d}/system.prmtop {d}/system.inpcrd
savepdb MOL {d}/system.pdb
quit
""")

    r = subprocess.run(
        ["tleap", "-f", str(tleap_in)],
        capture_output=True, text=True, cwd=str(d)
    )
    prmtop = d / "system.prmtop"
    inpcrd = d / "system.inpcrd"
    syspdb = d / "system.pdb"
    ok = prmtop.exists() and inpcrd.exists() and prmtop.stat().st_size > 1000

    if ok:
        # Count atoms
        n_atoms = sum(1 for l in syspdb.read_text().splitlines() if l.startswith("ATOM") or l.startswith("HETATM"))
        results[lig] = ("OK", n_atoms, prmtop.stat().st_size)
        print(f"  {lig:<10}: OK — {n_atoms} atoms, prmtop {prmtop.stat().st_size//1024} KB")
    else:
        err = (r.stdout + r.stderr)[-800:]
        results[lig] = ("FAILED", 0, 0)
        print(f"  {lig:<10}: FAILED")
        print("   ", err[-400:])
