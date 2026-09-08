
import shutil, os

src  = f"{WS}/kinome_selectivity_profile.md"
dst  = f"{WS}/reports/kinome_selectivity_profile.md"
shutil.copy2(src, dst)
print("Copied to reports/:", os.path.getsize(dst), "bytes")

# Also save master pivot as CSV for future reference
pivot.to_csv(f"{WS}/kinome_selectivity_matrix.csv")
print("Matrix CSV saved:", os.path.getsize(f"{WS}/kinome_selectivity_matrix.csv"), "bytes")
