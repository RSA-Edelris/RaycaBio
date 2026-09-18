
import subprocess, time, os

# Check CPD1 directory
print("=== CPD1 param dir ===")
cpd1_dir = PARAM_DIR / "CPD1"
for f in sorted(cpd1_dir.iterdir()):
    print(f"  {f.name:40s}  {f.stat().st_size:8d} bytes")

# Wait for CPD12
print("\nWaiting for CPD12 (pid 733634)...")
start = time.time()
while os.path.exists("/proc/733634"):
    elapsed = int(time.time() - start)
    if elapsed > 600:
        print(f"  still running at t={elapsed}s, giving more time...")
    if elapsed > 900:
        print("  killing CPD12 after 900s")
        subprocess.run(["kill", "733634"], capture_output=True)
        break
    time.sleep(30)
    print(f"  t={elapsed:3d}s still running")
    
mol2_12 = PARAM_DIR / "CPD12" / "CPD12.mol2"
print(f"\nCPD12 mol2: {'OK' if mol2_12.exists() else 'FAILED'}")
if not mol2_12.exists():
    rlog = PARAM_DIR / "CPD12" / "antechamber_retry.log"
    if rlog.exists():
        print(rlog.read_text()[-800:])
