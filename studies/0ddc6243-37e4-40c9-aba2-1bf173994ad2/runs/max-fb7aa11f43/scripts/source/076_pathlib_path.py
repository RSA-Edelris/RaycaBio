
import pathlib, re, subprocess

gaff2_dat = pathlib.Path("/home/ubuntu/rayca-runtime/.mamba/envs/rayca/dat/leap/parm/gaff2.dat")

# Use grep to find relevant torsion lines
r = subprocess.run(["grep", "-n", r"c1\|ce-n\|n -c\|ns-c\|c-ns", str(gaff2_dat)],
                   capture_output=True, text=True)
lines = r.stdout.strip().splitlines()
# Filter to lines that look like DIHE entries (have numeric fields)
for l in lines:
    if re.search(r'\d+\.\d+', l):
        print(l)
