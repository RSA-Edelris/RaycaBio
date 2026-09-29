
# Look broader — transcript may be in parent dirs or under /home/ubuntu
import subprocess
result = subprocess.run(
    ["find", "/home/ubuntu/rayca-sessions/318e1560-3d55-4b84-bafd-39c623c8d42c-c53814dd4ebb",
     "-name", "*.jsonl", "-o", "-name", "transcript*", "-o", "-name", "conversation*",
     "-o", "-name", "messages*", "-o", "-name", "journal*"],
    capture_output=True, text=True, timeout=15
)
print(result.stdout[:3000] or "(none found in session dir)")

# Also check one level up
result2 = subprocess.run(
    ["find", "/home/ubuntu/rayca-sessions", "-maxdepth", "3",
     "-name", "*.jsonl", "-o", "-name", "journal*", "-o", "-name", "transcript*"],
    capture_output=True, text=True, timeout=15
)
print("\nBroader search:")
print(result2.stdout[:3000] or "(none)")
