
import subprocess, pathlib, shutil

SESSION = pathlib.Path("/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b")
PARAM_DIR  = SESSION / "md" / "param"
SYSTEMS_DIR = SESSION / "md" / "systems"
RECEPTOR   = SESSION / "md" / "receptor_nozn.pdb"

# ── 1. Replace CPD4.frcmod with the complete version and re-run CPD7 parmchk2 with -a Y ──
shutil.copy(PARAM_DIR / "CPD4" / "CPD4_v2.frcmod",
            PARAM_DIR / "CPD4" / "CPD4.frcmod")
print("CPD4.frcmod replaced with -a Y version")

# Also re-generate CPD7 with -a Y
for lig in ["CPD7"]:
    d = PARAM_DIR / lig
    mol2 = d / f"{lig}_fixed.mol2"
    frc  = d / f"{lig}.frcmod"
    r = subprocess.run(
        ["parmchk2", "-i", str(mol2), "-f", "mol2", "-o", str(frc), "-s", "gaff2", "-a", "Y"],
        capture_output=True, text=True, cwd=str(d)
    )
    print(f"CPD7 parmchk2 rc={r.returncode}, frcmod={frc.stat().st_size} bytes")

# ── 2. Re-run tleap for CPD4 and CPD7 ──
for lig in ["CPD4", "CPD7"]:
    mol2   = PARAM_DIR / lig / f"{lig}_fixed.mol2"
    frcmod = PARAM_DIR / lig / f"{lig}.frcmod"
    d      = SYSTEMS_DIR / lig
    d.mkdir(exist_ok=True)

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
    ok = prmtop.exists() and inpcrd.exists() and prmtop.stat().st_size > 10000

    if ok:
        syspdb = d / "system.pdb"
        n_atoms = sum(1 for l in syspdb.read_text().splitlines() if l.startswith(("ATOM","HETATM")))
        print(f"  {lig}: OK — {n_atoms} atoms, prmtop {prmtop.stat().st_size//1024} KB")
    else:
        out = r.stdout + r.stderr
        errs = [l for l in out.splitlines() if "Error" in l or "Fatal" in l]
        print(f"  {lig}: FAILED — {errs[:5]}")
        print(out[-600:])
