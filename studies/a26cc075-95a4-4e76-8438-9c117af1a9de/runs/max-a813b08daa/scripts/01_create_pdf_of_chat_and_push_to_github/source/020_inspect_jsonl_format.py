
# Inspect the JSONL format
with open(TRANSCRIPT) as f:
    for i, line in enumerate(f):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            print(f"Line {i}: keys={list(obj.keys())}")
            if i >= 4:
                break
        except Exception as e:
            print(f"Line {i}: parse error {e}")
            break
