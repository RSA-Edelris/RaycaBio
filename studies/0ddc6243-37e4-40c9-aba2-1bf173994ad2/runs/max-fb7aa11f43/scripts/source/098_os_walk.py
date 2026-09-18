
import os

base = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b"

targets = [
    "progress.txt",
    "run_start.txt",
    "summary_table.txt",
    "CPD7_progress.txt",
    "audit_job_22076435_recovery.md",
]

found = []
for root, dirs, files in os.walk(base):
    for f in files:
        if f in targets:
            p = os.path.join(root, f)
            found.append(p)

for p in sorted(found):
    print(f"\n{'='*60}")
    print(p)
    print('='*60)
    print(open(p).read())
