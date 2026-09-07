
from pathlib import Path

dat = (Path(MMDIR) / "EDEL-CRBN-0001_ent" / "FINAL_RESULTS_MMPBSA.dat").read_text()
# Print the last 50 lines which contain the summary
lines = dat.split("\n")
for line in lines[-60:]:
    if line.strip():
        print(line)
