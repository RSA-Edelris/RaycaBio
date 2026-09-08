
import gzip, json

# Check full result_dock dict for the raw output
raw = result_dock.get("output_raw", "")
out = result_dock.get("output", {})
print("output keys:", list(out.keys()) if isinstance(out, dict) else type(out))
print("output_raw (first 500):", str(raw)[:500])

# Find the docked SDF file
import glob, os
gz_files = glob.glob(f"{ART}/*.sdf.gz") + glob.glob(f"{ART}/*.sdf")
print("\nSDF/GZ files in artifact dir:", gz_files)

# Also check the workspace
ws_gz = glob.glob(f"{WS}/*.sdf.gz") + glob.glob(f"{WS}/*.sdf")
print("SDF/GZ in workspace:", ws_gz)
