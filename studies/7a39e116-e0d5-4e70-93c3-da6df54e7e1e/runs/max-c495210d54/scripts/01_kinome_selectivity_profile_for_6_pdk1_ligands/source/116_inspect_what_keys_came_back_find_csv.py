
# Inspect what keys came back and find the CSV
print("Keys:", list(result_agc.keys()))
print()
# Check results field
r = result_agc.get("results")
if r:
    print("Type of results:", type(r))
    if isinstance(r, str):
        print("First 500 chars:", r[:500])
    elif isinstance(r, (list, dict)):
        print(repr(r)[:1000])

# Check for output files written by the container
import os, glob
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
# look for any CSV or parquet produced recently (last hour)
recent = []
for ext in ["csv", "parquet", "tsv", "txt", "json"]:
    for f in glob.glob(f"{WS}/**/*.{ext}", recursive=True):
        mt = os.path.getmtime(f)
        import time
        if time.time() - mt < 3600:
            recent.append((mt, f))
recent.sort(reverse=True)
print("\nRecent files (last hour):")
for mt, f in recent[:20]:
    sz = os.path.getsize(f)
    print(f"  {f}  ({sz} bytes)")
