
import subprocess

# parmchk2 for all 9 ligands
print("Running parmchk2...")
for lig in LIGS:
    d    = PARAM_DIR / lig
    mol2 = d / f"{lig}_fixed.mol2"
    frc  = d / f"{lig}.frcmod"
    r = subprocess.run(
        ["parmchk2", "-i", str(mol2), "-f", "mol2", "-o", str(frc), "-s", "gaff2"],
        capture_output=True, text=True, cwd=str(d)
    )
    ok = frc.exists() and frc.stat().st_size > 0
    print(f"  {lig:<10}: {'OK' if ok else 'FAILED'} rc={r.returncode} ({frc.stat().st_size if ok else 0} bytes)")
    if not ok:
        print("    stderr:", r.stderr[:200])
