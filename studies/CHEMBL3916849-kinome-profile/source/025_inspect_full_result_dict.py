
# Inspect full result dict
import json
print("Result keys:", list(result.keys()))
print("\nFull result (truncated):")
for k, v in result.items():
    val_str = str(v)
    print(f"  {k}: {val_str[:300]}")
