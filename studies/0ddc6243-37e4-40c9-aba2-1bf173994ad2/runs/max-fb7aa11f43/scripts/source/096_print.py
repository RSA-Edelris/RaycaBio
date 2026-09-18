
base = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b"

for path in [
    f"{base}/slurm-22076694.log",
    f"{base}/slurm-22076619.log",
    f"{base}/job-22076694/CPD8_progress.txt",
    f"{base}/job-22076619/progress.log",
]:
    print(f"\n===== {path.split('/')[-1]} =====")
    try:
        print(open(path).read())
    except Exception as e:
        print(f"ERROR: {e}")
