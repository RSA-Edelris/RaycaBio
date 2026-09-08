
import glob, os
# Check for report file
reports = glob.glob(f"{WS}/**/*.md", recursive=True) + glob.glob(f"{WS}/*.md")
for f in sorted(reports):
    print(os.path.getsize(f), f)
