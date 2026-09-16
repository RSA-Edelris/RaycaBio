
# Parse the SDF file to extract CAS numbers and MOL_NAMEs
sdf_path = "/home/ubuntu/rayca-artifacts/9b531d029532706a25e7a959/files/HTE_Edelris.sdf"

cas_numbers = []
mol_names = []

with open(sdf_path, 'r') as f:
    lines = f.readlines()

i = 0
current_cas = None
current_name = None

while i < len(lines):
    line = lines[i].strip()
    if line == ">  <CAS_NUMBER>":
        if i+1 < len(lines):
            current_cas = lines[i+1].strip()
    elif line == ">  <MOL_NAME>":
        if i+1 < len(lines):
            current_name = lines[i+1].strip()
    elif line == "$$$$":
        if current_cas or current_name:
            cas_numbers.append(current_cas)
            mol_names.append(current_name)
        current_cas = None
        current_name = None
    i += 1

print(f"Total compounds in SDF: {len(cas_numbers)}")
print("\nAll compounds:")
for i, (cas, name) in enumerate(zip(cas_numbers, mol_names)):
    print(f"  {i+1:3d}. CAS: {cas:20s}  NAME: {name}")
