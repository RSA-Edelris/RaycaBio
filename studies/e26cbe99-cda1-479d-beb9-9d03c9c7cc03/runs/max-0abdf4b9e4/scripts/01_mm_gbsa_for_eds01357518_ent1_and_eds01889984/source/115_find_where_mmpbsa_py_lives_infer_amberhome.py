
import subprocess
# find where MMPBSA.py lives and infer AMBERHOME
r = subprocess.run(["which", "MMPBSA.py"], capture_output=True, text=True)
print("MMPBSA.py:", r.stdout.strip())
r2 = subprocess.run(["find", "/home/ubuntu/rayca-runtime", "-name", "spc.xvv", "-maxdepth", "8"], capture_output=True, text=True)
print("spc.xvv:", r2.stdout.strip())
