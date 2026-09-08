
# Inspect dispatch and run_aidd_tool properly
try:
    print("=== dispatch doc ===")
    print(dispatch.__doc__[:2000] if dispatch.__doc__ else "no docstring")
except Exception as e:
    print(f"dispatch doc error: {e}")

try:
    print("\n=== run_aidd_tool doc ===")
    print(run_aidd_tool.__doc__[:2000] if run_aidd_tool.__doc__ else "no docstring")
except Exception as e:
    print(f"run_aidd_tool doc error: {e}")

# Also check what kwargs dispatch accepts
try:
    import inspect
    print("\ndispatch source (first 40 lines):")
    src = inspect.getsource(dispatch)
    print('\n'.join(src.split('\n')[:40]))
except Exception as e:
    print(f"getsource error: {e}")
