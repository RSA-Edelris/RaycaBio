
import json

# Load from the individual auto-saved files and inspect structure
with open("aizynthfinder-results.json") as fh:
    mcuf_raw = json.load(fh)

# Top-level keys
print("Top-level keys:", list(mcuf_raw.keys()))

# If it's the dispatch envelope
if "output" in mcuf_raw:
    out = mcuf_raw["output"]
    print("output keys:", list(out.keys()) if isinstance(out, dict) else type(out))
    if isinstance(out, dict) and "routes" in out:
        routes = out["routes"]
        print(f"n routes: {len(routes)}")
        if routes:
            r0 = routes[0]
            print("route[0] keys:", list(r0.keys()))
            # Print the full first route
            print(json.dumps(r0, indent=2)[:3000])
else:
    # Maybe the file IS the output directly
    print("Direct output keys:", list(mcuf_raw.keys()))
    if "routes" in mcuf_raw:
        routes = mcuf_raw["routes"]
        print(f"n routes: {len(routes)}")
        if routes:
            r0 = routes[0]
            print("route[0] keys:", list(r0.keys()))
            print(json.dumps(r0, indent=2)[:3000])
