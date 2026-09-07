
SESSION = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"

with open(f"{SESSION}/md_EDS01806218_ent1/mmpbsa_results.dat") as f:
    txt = f.read()

# Print the DELTA section and a check on absolute VDW
in_delta = False
vdw_complex = None
for line in txt.splitlines():
    if "DELTA TOTAL" in line or in_delta:
        in_delta = True
        print(line)
    if "VDWAALS" in line and "complex" in txt[:txt.find(line)].lower().split("complex")[-1][:5] if False else "VDWAALS" in line:
        pass

# Simpler: just print the whole result
print("\n=== Full results ===")
print(txt)
