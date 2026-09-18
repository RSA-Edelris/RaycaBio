
import subprocess, time, os

retry_pids = [733511, 733536, 733559, 733584, 733608, 733634]
start = time.time()
while True:
    alive = [p for p in retry_pids if os.path.exists(f"/proc/{p}")]
    elapsed = int(time.time() - start)
    if not alive:
        print(f"All 6 retries done at t={elapsed}s")
        break
    if elapsed > 600:
        print(f"Timeout — still alive: {alive}")
        for p in alive:
            subprocess.run(["kill", str(p)], capture_output=True)
        break
    time.sleep(30)
    print(f"  t={elapsed:3d}s  alive: {len(alive)}  pids: {alive}")

# Final status: all 9
print("\n=== Final antechamber status ===")
all_ok = True
for lig in LIGS:
    mol2 = PARAM_DIR / lig / f"{lig}.mol2"
    ok = mol2.exists() and mol2.stat().st_size > 100
    if not ok:
        all_ok = False
        # Check retry log
        rlog = PARAM_DIR / lig / "antechamber_retry.log"
        last = ""
        if rlog.exists():
            lines = rlog.read_text().splitlines()
            last = " | " + next((l for l in reversed(lines) if l.strip()), "empty")
        print(f"  {lig:<10}: FAILED{last}")
    else:
        print(f"  {lig:<10}: OK ({mol2.stat().st_size} bytes)")

print(f"\nAll OK: {all_ok}")
