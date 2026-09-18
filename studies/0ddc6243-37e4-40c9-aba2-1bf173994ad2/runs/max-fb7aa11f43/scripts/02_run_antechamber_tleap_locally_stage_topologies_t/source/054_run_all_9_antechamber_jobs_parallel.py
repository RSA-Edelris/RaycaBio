
import subprocess, os, time

# Run all 9 antechamber jobs in parallel
procs = {}
for lig in LIGS:
    d = PARAM_DIR / lig
    d.mkdir(exist_ok=True)
    sdf = LIG_DIR / f"{lig}_top.sdf"
    cmd = [
        "antechamber",
        "-i", str(sdf), "-fi", "sdf",
        "-o", str(d / f"{lig}.mol2"), "-fo", "mol2",
        "-c", "bcc", "-s", "2", "-nc", "0",
        "-rn", "LIG", "-at", "gaff2", "-dr", "no",
        "-pf", "y"   # purge intermediate files
    ]
    log = open(d / "antechamber.log", "w")
    p = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, cwd=str(d))
    procs[lig] = (p, log, time.time())
    print(f"  started {lig} (pid {p.pid})")

print(f"\n{len(procs)} antechamber jobs running in parallel...")
