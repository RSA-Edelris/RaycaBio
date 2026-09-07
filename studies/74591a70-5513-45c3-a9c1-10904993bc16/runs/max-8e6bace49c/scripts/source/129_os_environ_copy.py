
import subprocess, os
BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
AMBER_BIN = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin"
ENV = os.environ.copy()
ENV['PATH'] = AMBER_BIN + ':' + ENV.get('PATH', '')
ENV['AMBERHOME'] = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'

rec_in  = f"{BASE}/mmgbsa2/receptor_protein.pdb"
rec_out = f"{BASE}/mmgbsa2/receptor_amber.pdb"

# Run pdb4amber to properly name HIS -> HID/HIE/HIP
r = subprocess.run(
    [f"{AMBER_BIN}/pdb4amber", "-i", rec_in, "-o", rec_out, "--nohyd", "--dry"],
    capture_output=True, text=True, env=ENV
)
print("RC:", r.returncode)
print("STDOUT:", r.stdout[:2000])
print("STDERR:", r.stderr[:2000])
