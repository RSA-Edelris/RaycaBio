
# Understand the message structure
with open(TRANSCRIPT) as f:
    for i, line in enumerate(f):
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if 'message' in obj:
            msg = obj['message']
            print(f"Line {i}: type={obj.get('type')}, msg_keys={list(msg.keys()) if isinstance(msg,dict) else type(msg)}")
            if isinstance(msg, dict):
                role = msg.get('role')
                content = msg.get('content','')
                if isinstance(content, list):
                    for c in content[:2]:
                        print(f"  role={role}, content_type={c.get('type')}, text_preview={str(c.get('text',''))[:80]}")
                else:
                    print(f"  role={role}, content={str(content)[:80]}")
        if i >= 6:
            break
