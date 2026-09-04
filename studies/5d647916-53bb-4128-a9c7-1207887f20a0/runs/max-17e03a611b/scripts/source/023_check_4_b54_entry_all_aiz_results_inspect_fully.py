
import json

# ── CHECK 4: B54 entry in all_aiz_results — inspect fully ─────────────────
with open("/home/ubuntu/rayca-sessions/5d647916-53bb-4128-a9c7-1207887f20a0-d11115b837f3/all_aiz_results.json") as f:
    all_results = json.load(f)

print("Top-level keys in all_aiz_results.json:", list(all_results.keys()))

b54 = all_results.get("B54", None)
if b54:
    print("\nB54 entry:")
    print(f"  rc:           {b54.get('rc')!r}")
    print(f"  error:        {b54.get('error')!r}")
    print(f"  duration_s:   {b54.get('duration_s')!r}")
    print(f"  image:        {b54.get('image')!r}")
    print(f"  gpu:          {b54.get('gpu')!r}")
    print(f"  summary:      {b54.get('summary')!r}")
    print(f"  unstaged:     {b54.get('unstaged')!r}")
else:
    print("No B54 key found")

# Also check batch1 file for B54
with open("/home/ubuntu/rayca-sessions/5d647916-53bb-4128-a9c7-1207887f20a0-d11115b837f3/aiz_results_batch1.json") as f:
    batch1 = json.load(f)
print("\nKeys in aiz_results_batch1.json:", list(batch1.keys()) if isinstance(batch1, dict) else type(batch1))
if isinstance(batch1, dict) and "B54" in batch1:
    print("B54 also in batch1:", batch1["B54"].get("rc"), batch1["B54"].get("error"))
