
import json

# Inspect top-level keys and route structure from each result
for name, r in aizyn_results.items():
    print(f"\n{'='*60}")
    print(f"TARGET: {name}")
    print(f"Top-level keys: {list(r.keys())}")
    for k, v in r.items():
        if k == "routes":
            print(f"  routes: {len(v) if isinstance(v, list) else type(v)} items")
            if isinstance(v, list) and len(v) > 0:
                print(f"    route[0] keys: {list(v[0].keys()) if isinstance(v[0], dict) else type(v[0])}")
        elif k == "statistics":
            print(f"  statistics: {v}")
        elif k == "summary":
            print(f"  summary: {str(v)[:300]}")
        else:
            print(f"  {k}: {v}")
