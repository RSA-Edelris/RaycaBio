
import pathlib, re

gaff2_dat = pathlib.Path("/home/ubuntu/rayca-runtime/.mamba/envs/rayca/dat/leap/parm/gaff2.dat")
text = gaff2_dat.read_text()

# Show section headers
print("Section starts:")
for i, l in enumerate(text.splitlines()):
    if re.match(r'^[A-Z]{2,}', l) and len(l) < 30:
        print(f"  line {i}: {repr(l)}")

print("\nLines 1-5:")
for i, l in enumerate(text.splitlines()[:5]):
    print(repr(l))
