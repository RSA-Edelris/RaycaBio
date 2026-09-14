
import subprocess, os, time

BOLTZ_BIN = '/home/ubuntu/rayca-sessions/.session-libs/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/bin/boltz'
YAML      = '/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/ARV471_ERalpha_CRBN_boltz_input.yaml'
OUT_DIR   = '/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/boltz_cpu_out'
LOG_FILE  = '/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/boltz_cpu.log'

os.makedirs(OUT_DIR, exist_ok=True)

env = {**os.environ, 'PYTHONUNBUFFERED': '1',
       'PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION': 'python'}

cmd = [
    BOLTZ_BIN, 'predict', YAML,
    '--out_dir', OUT_DIR,
    '--accelerator', 'cpu',
    '--diffusion_samples', '3',
    '--recycling_steps', '1',
    '--sampling_steps', '50',
    '--output_format', 'pdb',
    '--num_workers', '0',
    '--no_kernels',
    '--seed', '42',
]

log_fh = open(LOG_FILE, 'w')
proc = subprocess.Popen(cmd, stdout=log_fh, stderr=subprocess.STDOUT, env=env)
with open('/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/boltz_cpu.pid', 'w') as f:
    f.write(str(proc.pid))
print(f"PID={proc.pid}")

# Wait 50s then check — longer now that imports+checkpoint load takes ~30s
time.sleep(50)
if proc.poll() is not None:
    with open(LOG_FILE) as lf:
        print("Exited:", lf.read()[-2000:])
else:
    with open(LOG_FILE) as lf:
        log = lf.read()
    lines = [l for l in log.splitlines() if l.strip()]
    print("Running. Tail:\n" + '\n'.join(lines[-10:]))
