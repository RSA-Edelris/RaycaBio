
# The result is a special dict - let's iterate its items carefully
for k, v in result.items():
    vtype = type(v).__name__
    if isinstance(v, str):
        print(f"{k} ({vtype}): {v[:200]}")
    elif isinstance(v, (int, float, bool, type(None))):
        print(f"{k} ({vtype}): {v}")
    elif isinstance(v, list):
        print(f"{k} (list, len={len(v)}): {v}")
    elif isinstance(v, dict):
        print(f"{k} (dict, keys={list(v.keys())})")
    else:
        print(f"{k} ({vtype}): {repr(v)[:100]}")
