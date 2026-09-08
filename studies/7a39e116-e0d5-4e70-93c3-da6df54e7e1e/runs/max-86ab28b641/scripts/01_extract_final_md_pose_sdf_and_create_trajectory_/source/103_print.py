
import subprocess, shutil

py = "/home/ubuntu/rayca-runtime/.venv/bin/python3"

for tool in ["ffmpeg", "convert"]:
    print(f"{tool}: {shutil.which(tool) or 'NOT FOUND'}")

r = subprocess.run([py, "-c", """
import matplotlib
import matplotlib.animation as anim
print("matplotlib:", matplotlib.__version__)
print("writers:", anim.writers.list())
"""], capture_output=True, text=True, timeout=15)
print(r.stdout)
if r.returncode != 0:
    print("err:", r.stderr[:200])
