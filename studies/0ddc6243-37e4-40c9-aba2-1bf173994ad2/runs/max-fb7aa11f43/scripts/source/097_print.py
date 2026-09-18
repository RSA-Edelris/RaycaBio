
base = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b"

print("===== REF_85C min.mdinfo =====")
print(open(f"{base}/job-22076619/md_work/run_REF_85C/min.mdinfo").read())

print("\n===== REF_85C min.out (last 40 lines) =====")
lines = open(f"{base}/job-22076619/md_work/run_REF_85C/min.out").readlines()
print("".join(lines[-40:]))
