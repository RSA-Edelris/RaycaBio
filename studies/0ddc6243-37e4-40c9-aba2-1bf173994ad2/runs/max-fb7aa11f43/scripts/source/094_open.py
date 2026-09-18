
jobdir = f"{base}/job-22076592"

# Read SLURM log
with open(f"{base}/slurm-22076592.log") as f:
    print("=== slurm-22076592.log ===")
    print(f.read())

# Read job log
with open(f"{jobdir}/jobA_log.txt") as f:
    print("\n=== jobA_log.txt ===")
    print(f.read())

# Inspect tarballs
import tarfile, io
for name in ["analysis_A.tar.gz", "mdlogs_A.tar.gz"]:
    path = f"{jobdir}/{name}"
    size = os.path.getsize(path)
    print(f"\n=== {name} ({size} bytes) ===")
    try:
        with tarfile.open(path) as tf:
            members = tf.getnames()
            print(f"  Members ({len(members)}): {members[:20]}")
    except Exception as e:
        print(f"  Could not open: {e}")
