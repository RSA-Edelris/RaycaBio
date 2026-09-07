
import subprocess, os
AMBERHOME = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
env = {**os.environ, 'AMBERHOME': AMBERHOME}
r = subprocess.run(['ante-MMPBSA.py', '--help'], capture_output=True, text=True, env=env)
print(r.stdout[:2000])
print(r.stderr[:2000])
