
import time, os, subprocess

# Poll every 2 minutes for up to 30 minutes, watching for prediction progress
for i in range(15):
    time.sleep(120)
    
    with open(LOG_FILE) as f:
        log = f.read()
    
    r = subprocess.run(['ps', '-p', '3619539', '-o', 'pid,stat,etime', '--no-headers'],
                       capture_output=True, text=True)
    alive = bool(r.stdout.strip())
    
    # Find the last meaningful log lines (skip tqdm noise)
    lines = [l for l in log.splitlines() if l.strip() and '|' not in l[:5]]
    tail = '\n'.join(lines[-8:])
    
    print(f"[{(i+1)*2}min] alive={alive}")
    print(f"Tail:\n{tail}\n---")
    
    done_signals = ['Writing predictions', 'Prediction done', 'Epoch', 'predict_step']
    error_signals = ['Error', 'Traceback', 'FAILED', 'exception']
    
    if any(s.lower() in log.lower() for s in error_signals):
        print("ERROR detected!")
        print(log[-2000:])
        break
    if any(s in log for s in done_signals):
        print("DONE or making good progress!")
        break
    if not alive:
        print("Process exited. Full log:")
        print(log)
        break
    
    # Also list output dir for any results
    for root, dirs, files in os.walk(OUT_DIR):
        for fn in files:
            fp = os.path.join(root, fn)
            print(f"  output: {fp} ({os.path.getsize(fp)}b)")
