
import os

# Check the JSONL transcript
path = os.path.expanduser(
    '~/.claude/projects/-home-ubuntu-rayca-sessions-318e1560-3d55-4b84-bafd-39c623c8d42c-c53814dd4ebb'
    '/302c604b-837c-4739-b5da-bd16709541b5.jsonl'
)
print("Exists:", os.path.exists(path))
if os.path.exists(path):
    sz = os.path.getsize(path)
    print(f"Size: {sz:,} bytes ({sz/1024/1024:.1f} MB)")
    # peek at first few lines
    with open(path) as f:
        for i, line in enumerate(f):
            if i >= 4:
                break
            print(f"\nLine {i}: {line[:300]}")
