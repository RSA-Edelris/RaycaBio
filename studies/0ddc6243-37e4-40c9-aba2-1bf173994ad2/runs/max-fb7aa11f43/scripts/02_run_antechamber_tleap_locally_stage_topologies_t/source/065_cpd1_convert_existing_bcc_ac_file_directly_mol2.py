
import subprocess

# CPD1: convert existing BCC AC file directly to mol2
d1 = PARAM_DIR / "CPD1"
r = subprocess.run(
    ["antechamber",
     "-i", "ANTECHAMBER_AM1BCC.AC", "-fi", "ac",
     "-o", "CPD1.mol2", "-fo", "mol2",
     "-at", "gaff2", "-rn", "LIG", "-dr", "no"],
    capture_output=True, text=True, cwd=str(d1)
)
print("stdout:", r.stdout[-500:])
print("stderr:", r.stderr[-500:])

mol2 = d1 / "CPD1.mol2"
print(f"mol2 exists: {mol2.exists()}, size: {mol2.stat().st_size if mol2.exists() else 0} bytes")

# Final status: all 9
print("\n=== ALL 9 LIGANDS STATUS ===")
all_ok = True
for lig in LIGS:
    mol2 = PARAM_DIR / lig / f"{lig}.mol2"
    ok = mol2.exists() and mol2.stat().st_size > 100
    if not ok: all_ok = False
    print(f"  {lig:<10}: {'OK' if ok else 'FAILED'}")
print(f"\nAll mol2 ready: {all_ok}")
