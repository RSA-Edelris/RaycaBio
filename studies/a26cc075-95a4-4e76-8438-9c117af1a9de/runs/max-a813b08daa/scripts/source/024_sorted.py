
import os

PROJ = "/home/ubuntu/.claude/projects/-home-ubuntu-rayca-sessions-a26cc075-95a4-4e76-8438-9c117af1a9de-26995afd3529/"
files = sorted([f for f in os.listdir(PROJ) if f.endswith('.jsonl')])

# Scan all files for text content blocks
all_turns = []
for fname in files:
    path = os.path.join(PROJ, fname)
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except:
                continue
            if obj.get('isSidechain'):
                continue
            msg = obj.get('message', {})
            if not isinstance(msg, dict):
                continue
            role = msg.get('role')
            if role not in ('user', 'assistant'):
                continue
            content = msg.get('content', [])
            ts = obj.get('timestamp', '')
            text_blocks = []
            if isinstance(content, list):
                for b in content:
                    if isinstance(b, dict) and b.get('type') == 'text':
                        t = b.get('text', '').strip()
                        if t:
                            text_blocks.append(t)
            elif isinstance(content, str) and content.strip():
                text_blocks.append(content.strip())
            if text_blocks:
                all_turns.append((ts, role, '\n'.join(text_blocks), fname))

print(f"Total text turns across all files: {len(all_turns)}")
for ts, role, text, fn in all_turns[:8]:
    print(f"[{fn[:8]}] [{role}] {text[:100]}")
