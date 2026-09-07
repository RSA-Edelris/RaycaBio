
import json

# Check what keys the result actually has
for name, r in missing_results.items():
    print(f"\n{name}:")
    if isinstance(r, dict):
        for k, v in r.items():
            if k != 'poses':  # skip long list
                print(f"  {k}: {v}")
    else:
        print(f"  type={type(r)}, value={r}")
