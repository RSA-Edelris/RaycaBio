
# Check full output dict from the docking run
output = result['output']
for k, v in output.items():
    if isinstance(v, str):
        print(f"{k}: {v[:300]}")
    else:
        print(f"{k}: {v}")
