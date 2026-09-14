
# Print full error output
import json
print("=== FULL RESULT KEYS ===")
print(list(result.keys()))
print("\n=== STDERR (full) ===")
print(result.get('stderr', '(none)'))
print("\n=== STDOUT (full) ===")
print(result.get('stdout', '(none)'))
print("\n=== ERROR ===")
print(result.get('error', '(none)'))
