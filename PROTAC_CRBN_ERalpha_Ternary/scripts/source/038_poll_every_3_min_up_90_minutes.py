
import time, os, subprocess

# Poll every 3 min for up to 90 minutes
for i in range(30):
    time.sleep(180)
    
    with open(LOG_FILE) as f:
        log = f.read()
    
    r = subprocess.run(['ps', '-p', '3638479', '-o', 'pid,stat,etime', '--no-headers'],
                       capture_output=True, text=True)
    alive = bool(r.stdout.strip())
    elapsed = r.stdout.strip().split()[-1] if alive else "done"
    
    clean = [l for l in log.splitlines() 
             if l.strip() and 'File "' not in l and '__pycache__' not in l]
    tail = '\n'.join(clean[-8:])
    
    print(f"[{(i+1)*3}min] alive={alive} elapsed={elapsed}")
    print(f"Tail:\n{tail}\n")
    
    if any(s in log for s in ['Writing predictions', 'predict_step', 'Predicting:', 'it/s', '%|']):
        print("Progress detected! Continuing watch...")
    
    if any(s.lower() in log.lower() for s in ['traceback', 'error', 'exception', 'killed']):
        print("ERROR:")
        print(log[-3000:])
        break
    
    if not alive:
        print("Process finished. Final log:")
        print(log[-3000:])
        # Check output files
        print("\nOutput files:")
        for root, dirs, files in os.walk(OUT_DIR):
            for fn in files:
                fp = os.path.join(root, fn)
                print(f"  {fp} ({os.path.getsize(fp)} bytes)")
        break
