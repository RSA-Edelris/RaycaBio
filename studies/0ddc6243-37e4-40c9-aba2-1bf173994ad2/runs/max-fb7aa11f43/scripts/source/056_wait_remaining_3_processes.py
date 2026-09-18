
import subprocess, time, os

# Wait for remaining 3 processes
still_alive = [636200, 636211, 636224]
start = time.time()
while True:
    alive = [p for p in still_alive if os.path.exists(f"/proc/{p}")]
    if not alive:
        print(f"All done at t={int(time.time()-start)}s")
        break
    if time.time() - start > 600:
        print(f"Timeout — still alive: {alive}")
        # Kill stuck ones
        for p in alive:
            subprocess.run(["kill", str(p)], capture_output=True)
        break
    time.sleep(30)

# Check final status
print("\nFinal mol2 status:")
ok_ligs, fail_ligs = [], []
for lig in LIGS:
    mol2 = PARAM_DIR / lig / f"{lig}.mol2"
    if mol2.exists() and mol2.stat().st_size > 100:
        ok_ligs.append(lig)
        print(f"  {lig:<10}: OK ({mol2.stat().st_size} bytes)")
    else:
        fail_ligs.append(lig)
        print(f"  {lig:<10}: FAILED")

print(f"\nOK: {len(ok_ligs)}  FAILED: {len(fail_ligs)}")
print(f"Failed: {fail_ligs}")

# Check full log for one failed compound to diagnose
print("\n--- REF_85C antechamber.log ---")
log_path = PARAM_DIR / "REF_85C" / "antechamber.log"
if log_path.exists():
    print(log_path.read_text()[-2000:])
