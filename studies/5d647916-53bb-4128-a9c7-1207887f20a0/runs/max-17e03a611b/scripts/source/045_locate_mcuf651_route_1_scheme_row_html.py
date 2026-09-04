
# Locate the MCUF651 Route 1 scheme-row in the HTML
path = '/home/ubuntu/rayca-sessions/5d647916-53bb-4128-a9c7-1207887f20a0-d11115b837f3/synthetic_schemes.html'
with open(path) as f:
    html = f.read()

# Find start of MCUF651 section
sec_start = html.find('id="MCUF651"')
# Find the next top-level section after it
sec_end = html.find('<section ', sec_start + 100)

mcuf_chunk = html[sec_start:sec_end]

# Strip base64 for searching
clean = re.sub(r'data:image/svg\+xml;base64,[A-Za-z0-9+/=]+', 'B64', mcuf_chunk)

# Find the scheme-row div (first one = Route 1)
row_start = clean.find('<div class="scheme-row">')
row_end   = clean.find('</div>', row_start)
# scheme-row can be nested; find the closing </div> after all content
# count divs
depth = 0
i = row_start
while i < len(clean):
    if clean[i:i+4] == '<div':
        depth += 1
    elif clean[i:i+6] == '</div>':
        depth -= 1
        if depth == 0:
            row_end = i + 6
            break
    i += 1

print(f"MCUF651 section: chars {sec_start}–{sec_end}")
print(f"Route-1 scheme-row (in clean): chars {row_start}–{row_end}")
print(f"Row length (clean): {row_end - row_start}")

# Identify absolute positions in original html
# row_start is offset within mcuf_chunk in the *clean* version; need offset in original
# Better: search for the scheme-row in original html between sec_start and sec_end
orig_row_start = html.find('<div class="scheme-row">', sec_start, sec_end)
# Walk div depth to find closing tag
depth = 0
i = orig_row_start
while i < len(html):
    if html[i:i+4] == '<div':
        depth += 1
    elif html[i:i+6] == '</div>':
        depth -= 1
        if depth == 0:
            orig_row_end = i + 6
            break
    i += 1

print(f"\nOriginal HTML row: {orig_row_start}–{orig_row_end} ({orig_row_end - orig_row_start} chars)")
print("First 400 chars of row (no base64):")
snippet = re.sub(r'data:image/svg\+xml;base64,[A-Za-z0-9+/=]+', 'B64', html[orig_row_start:orig_row_start+1200])
print(snippet[:800])
