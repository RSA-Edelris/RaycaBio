
import subprocess, os, time

BOLTZ_BIN = '/home/ubuntu/rayca-sessions/.session-libs/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/bin/boltz'
YAML      = '/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/ARV471_ERalpha_CRBN_boltz_input.yaml'
OUT_DIR   = '/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/boltz_cpu_out'
LOG_FILE  = '/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/boltz_cpu.log'

os.makedirs(OUT_DIR, exist_ok=True)

cmd = [
    BOLTZ_BIN, 'predict', YAML,
    '--output_dir', OUT_DIR,
    '--diffusion_samples', '3',
    '--recycling_steps', '1',      # 1 instead of 3  (3x faster trunk)
    '--sampling_steps', '50',      # 50 instead of 200 (4x faster diffusion)
    '--output_format', 'pdb',
    '--num_workers', '0',          # CRITICAL: no subprocess workers
    '--no_kernels',                # CPU-safe (no triton/CUDA kernels)
    '--seed', '42',
]

log_fh = open(LOG_FILE, 'w')
proc = subprocess.Popen(cmd, stdout=log_fh, stderr=subprocess.STDOUT, 
                        env={**os.environ, 'PYTHONUNBUFFERED': '1'})

print(f"Launched PID={proc.pid}")
print(f"Log: {LOG_FILE}")
print(f"Output dir: {OUT_DIR}")

# save PID for later checks
with open('/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/boltz_cpu.pid', 'w') as f:
    f.write(str(proc.pid))

# Give it 5 seconds to start and check for immediate crash
time.sleep(5)
if proc.poll() is not None:
    print(f"CRASHED early with rc={proc.returncode}")
    with open(LOG_FILE) as f:
        print(f.read()[:2000])
else:
    print("Process still running after 5s — good.")
