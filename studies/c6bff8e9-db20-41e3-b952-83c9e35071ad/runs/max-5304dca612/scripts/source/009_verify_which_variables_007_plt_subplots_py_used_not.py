
# Verify which variables in 007_plt_subplots.py are used but not defined in that file

with open("/home/ubuntu/rayca-sessions/c6bff8e9-db20-41e3-b952-83c9e35071ad-9b531d029532/source/007_plt_subplots.py", 'r') as f:
    script_007 = f.read()

# Check for variables defined in 006 that 007 uses but doesn't define
vars_from_006 = ["CATALYSTS", "SOLVENTS", "BASES", "ROWS", "BASE_ROW_ALPHA", "SOLVENT_BG"]

print("=== Variables used in 007 but NOT defined in 007 ===")
import re
# Find all assignments in 007
defined_in_007 = set(re.findall(r'^([A-Z_]+)\s*=', script_007, re.MULTILINE))
print(f"Variables defined in 007: {sorted(defined_in_007)}")
print()
for v in vars_from_006:
    used = v in script_007
    defined = v in defined_in_007
    print(f"  {v:20s}  used={used}  defined_in_007={defined}  MISSING={used and not defined}")

print()
print("=== First line where each missing variable appears ===")
lines = script_007.split('\n')
for v in vars_from_006:
    if v in script_007 and v not in defined_in_007:
        for i, line in enumerate(lines, 1):
            if v in line:
                print(f"  {v:20s} first use: line {i}: {line.strip()}")
                break

print()
# Check 006 defines all of them
with open("/home/ubuntu/rayca-sessions/c6bff8e9-db20-41e3-b952-83c9e35071ad-9b531d029532/source/006_plate_2_design_4_bases_2_solvents_12_pd_catalysts_96.py", 'r') as f:
    script_006 = f.read()

defined_in_006 = set(re.findall(r'^([A-Z_]+)\s*=', script_006, re.MULTILINE))
print(f"Variables defined in 006: {sorted(defined_in_006)}")
print()
for v in vars_from_006:
    print(f"  {v:20s} defined in 006: {v in defined_in_006}")
