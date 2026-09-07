
# Inspect what dispatch/run_aidd_tool look like in this namespace
import inspect

# Check what's available
for name in ["dispatch", "run_aidd_tool", "aidd_tool_schema", "stage_file"]:
    obj = globals().get(name) or __builtins__.__dict__.get(name, None) if hasattr(__builtins__, '__dict__') else None
    if obj is None:
        try:
            import builtins
            obj = getattr(builtins, name, None)
        except:
            pass
    if obj is not None:
        try:
            sig = str(inspect.signature(obj))
            print(f"{name}{sig}")
        except Exception as e:
            print(f"{name}: {obj} (sig err: {e})")
    else:
        # try to find in globals
        g = {k:v for k,v in globals().items() if name.lower() in k.lower()}
        print(f"{name}: NOT found | similar globals: {list(g.keys())[:5]}")
