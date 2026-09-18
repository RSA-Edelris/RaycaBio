
import subprocess, time, os

# Check CPD1 failure
print("=== CPD1 retry log ===")
log = (PARAM_DIR / "CPD1" / "antechamber_retry.log").read_text()
print(log[-3000:])
