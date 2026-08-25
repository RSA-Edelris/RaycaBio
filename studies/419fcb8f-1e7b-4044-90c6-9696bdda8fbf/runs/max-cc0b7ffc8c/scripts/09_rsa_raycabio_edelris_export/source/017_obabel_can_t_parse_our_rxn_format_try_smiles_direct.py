
# obabel can't parse our RXN format — try SMILES-direct input
import subprocess, os

test = subprocess.run(
    ["obabel", "-:C1CCCCC1", "--gen2D", "-O", "/tmp/test_obabel.cdxml"],
    capture_output=True, text=True
)
print("smiles-direct:", test.returncode, test.stderr[:100])
print("file exists:", os.path.exists("/tmp/test_obabel.cdxml"),
      os.path.getsize("/tmp/test_obabel.cdxml") if os.path.exists("/tmp/test_obabel.cdxml") else 0)

# Also check what obabel can actually read
fmt_check = subprocess.run(["obabel", "-L", "formats", "read"], capture_output=True, text=True)
rxn_lines = [l for l in fmt_check.stdout.splitlines() if "rxn" in l.lower() or "mdl" in l.lower()]
print("RXN-related formats:", rxn_lines[:5])
