
# Inspect the actual structure of one result
import json

for fname, r in results.items():
    print(f"\n=== {fname} ===")
    if isinstance(r, dict):
        for k, v in r.items():
            if k == 'poses':
                print(f"  poses: {len(v) if isinstance(v, list) else type(v)}")
                if isinstance(v, list) and len(v) > 0:
                    print(f"    pose[0] keys: {list(v[0].keys()) if isinstance(v[0], dict) else type(v[0])}")
            elif k == 'output_file':
                print(f"  output_file: {v}")
            elif k == 'summary':
                print(f"  summary: {str(v)[:200]}")
            else:
                print(f"  {k}: {v}")
    else:
        print(f"  type={type(r)}, val={str(r)[:200]}")
    break  # just first one
