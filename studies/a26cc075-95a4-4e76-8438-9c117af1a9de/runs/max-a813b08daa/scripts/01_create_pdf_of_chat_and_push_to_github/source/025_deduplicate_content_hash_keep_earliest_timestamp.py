
import hashlib, textwrap

# Deduplicate by content hash, keep earliest timestamp
seen = {}
for ts, role, text, fn in all_turns:
    h = hashlib.md5(text.encode()).hexdigest()
    if h not in seen:
        seen[h] = (ts, role, text)

deduped = sorted(seen.values(), key=lambda x: x[0])

# Filter: keep actual user inputs (skip system/image lines) and assistant text
def is_human_message(text):
    skip = ['[Image:', 'Base directory for this skill:', '<system-reminder>', 'Stop hook', 'SessionStart hook']
    return not any(s in text for s in skip)

turns_pdf = [(role, text) for ts, role, text in deduped
             if role == 'user' and is_human_message(text)
             or role == 'assistant']

print(f"Turns for PDF: {len(turns_pdf)}")
for role, text in turns_pdf[:6]:
    print(f"[{role}] {text[:90]}")
