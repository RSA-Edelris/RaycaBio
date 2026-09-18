
import subprocess, time, os

PIDS = [636198, 636199, 636200, 636203, 636206, 636208, 636211, 636218, 636224]

# Poll until all done or 8 minutes elapsed
start = time.time()
while True:
    alive = [p for p in PIDS if os.path.exists(f"/proc/{p}")]
    elapsed = int(time.time() - start)
    print(f"  t={elapsed:3d}s  alive: {len(alive)}/{len(PIDS)}  {alive[:3]}{'...' if len(alive)>3 else ''}")
    if not alive:
        break
    if elapsed > 480:
        print("  timeout")
        break
    time.sleep(20)

# Check results
print("\nResults:")
for lig in LIGS:
    mol2 = PARAM_DIR / lig / f"{lig}.mol2"
    log  = PARAM_DIR / lig / "antechamber.log"
    ok   = mol2.exists() and mol2.stat().st_size > 100
    # Grab last error line if failed
    tail = ""
    if not ok and log.exists():
        lines = log.read_text().splitlines()
        tail = " | " + next((l for l in reversed(lines) if l.strip()), "empty log")
    print(f"  {lig:<10}: {'OK' if ok else 'FAILED'}{tail}")
