
import subprocess, os

r = subprocess.run(['ps', '-p', '3638479', '--no-headers', '-o', 'stat,etime,pcpu'],
                   capture_output=True, text=True)
print("Process:", r.stdout.strip() or "EXITED")

pdbs = subprocess.run(['find',
    '/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/boltz_cpu_out',
    '-name', '*.pdb', '-o', '-name', 'confidence*'],
    capture_output=True, text=True)
print("PDB/confidence files:", pdbs.stdout.strip() or "none yet")

log_size = os.path.getsize('/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/boltz_cpu.log')
print(f"Log size: {log_size} bytes")
