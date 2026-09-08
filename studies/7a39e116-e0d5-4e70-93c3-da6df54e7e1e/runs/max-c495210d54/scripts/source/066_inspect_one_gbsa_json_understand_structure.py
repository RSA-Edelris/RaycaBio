
# Inspect one GBSA JSON to understand structure
with open(f"{ART}/gbsa_EL2003A-A2U1.json") as f:
    sample = json.load(f)

print("Top-level keys:", list(sample.keys()))
print("rc:", sample.get('rc'))

# Look at 'results' structure
results = sample.get('results', [])
print(f"\n{len(results)} result entries")
if results:
    print("First result keys:", list(results[0].keys()))
    print("First result:", results[0])
    if len(results) > 1:
        print("Second result:", results[1])

# Also check output structure
out = sample.get('output', {})
print("\nOutput keys:", list(out.keys()) if isinstance(out, dict) else type(out))
