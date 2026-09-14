
import time, os, subprocess

# Check weight download progress every 30s for up to 5 minutes
for i in range(10):
    time.sleep(30)
    
    with open(LOG_FILE) as f:
        log = f.read()
    
    # Check download file sizes
    ckpt = '/home/ubuntu/.boltz/boltz2_conf.ckpt'
    mols_tar = '/home/ubuntu/.boltz/mols.tar'
    ckpt_size = os.path.getsize(ckpt) if os.path.exists(ckpt) else 0
    mols_size = os.path.getsize(mols_tar) if os.path.exists(mols_tar) else 0
    
    r = subprocess.run(['ps', '-p', '3601076', '-o', 'pid,stat', '--no-headers'],
                       capture_output=True, text=True)
    alive = bool(r.stdout.strip())
    
    print(f"[{(i+1)*30}s] alive={alive} | ckpt={ckpt_size/1e6:.1f}MB | mols.tar={mols_size/1e6:.1f}MB | log_tail={log[-200:].strip()}")
    
    # Stop early if past downloads
    if 'Processing' in log or 'Predicting' in log or 'Error' in log.lower():
        print("  => significant event detected")
        print("Full log:", log)
        break
    if not alive:
        print("Process exited!")
        print("Full log:", log)
        break
