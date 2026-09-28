
import json, textwrap, re

TRANSCRIPT = "/home/ubuntu/.claude/projects/-home-ubuntu-rayca-sessions-a26cc075-95a4-4e76-8438-9c117af1a9de-26995afd3529/e5698a81-f34a-4713-b98a-b8e5deaf9219.jsonl"

messages = []
with open(TRANSCRIPT) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except:
            continue
        role = obj.get("role")
        if role not in ("user", "assistant"):
            continue
        content = obj.get("content", "")
        if isinstance(content, list):
            text = " ".join(
                c.get("text", "") for c in content
                if isinstance(c, dict) and c.get("type") == "text"
            )
        else:
            text = str(content)
        text = text.strip()
        if text:
            messages.append((role, text))

print(f"Extracted {len(messages)} messages")
for role, text in messages[:3]:
    print(f"[{role}] {text[:120]}")
