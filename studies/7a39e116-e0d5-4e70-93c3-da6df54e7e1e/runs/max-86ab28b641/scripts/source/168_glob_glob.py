
import os, glob
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
# Check workspace root and reports/ for the chembl tool selection phase doc
for pat in ["*chembl_tool*", "*chembl_rest*", "*tool_select*", "*rest_api*"]:
    hits = glob.glob(f"{WS}/{pat}") + glob.glob(f"{WS}/reports/{pat}")
    for h in hits:
        print(os.path.basename(h), os.path.getsize(h))
print("---")
# Also list all phase_*.md at workspace root (most recent 10)
roots = sorted(glob.glob(f"{WS}/phase_*.md"), key=os.path.getmtime, reverse=True)[:10]
for f in roots:
    print(os.path.basename(f), os.path.getsize(f))
