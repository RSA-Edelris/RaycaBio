
# Extract readable human/assistant text from transcript
messages_clean = []
with open(TRANSCRIPT) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if obj.get('isSidechain'):
            continue
        msg = obj.get('message')
        if not isinstance(msg, dict):
            continue
        role = msg.get('role')
        if role not in ('user', 'assistant'):
            continue
        content = msg.get('content', [])
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            btype = block.get('type')
            if btype == 'text':
                text = block.get('text', '').strip()
                if text:
                    messages_clean.append((role, text))
                    break  # one text block per message turn

print(f"Found {len(messages_clean)} turns")
for r, t in messages_clean[:5]:
    print(f"[{r}] {t[:100]}")
