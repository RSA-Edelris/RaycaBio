
# Look deeper - dump actual content blocks
with open(TRANSCRIPT) as f:
    all_lines = [json.loads(l.strip()) for l in f if l.strip()]

# Find lines with user text messages (not tool_result)
for i, obj in enumerate(all_lines[:50]):
    if obj.get('isSidechain'):
        continue
    msg = obj.get('message', {})
    if not isinstance(msg, dict):
        continue
    role = msg.get('role')
    content = msg.get('content', [])
    if isinstance(content, list):
        for b in content:
            if isinstance(b, dict) and b.get('type') == 'text':
                print(f"Line {i} [{role}]: {b.get('text','')[:120]}")
                break
    elif isinstance(content, str) and content.strip():
        print(f"Line {i} [{role}] str: {content[:120]}")

print("---")
print(f"Total lines: {len(all_lines)}")
# Count by type
from collections import Counter
btypes = Counter()
for obj in all_lines:
    msg = obj.get('message', {})
    if isinstance(msg, dict):
        for b in (msg.get('content') or []):
            if isinstance(b, dict):
                btypes[b.get('type')] += 1
print("Content block types:", dict(btypes))
