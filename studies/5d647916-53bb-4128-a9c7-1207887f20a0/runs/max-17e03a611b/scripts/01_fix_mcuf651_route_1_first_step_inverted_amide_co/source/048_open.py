
path = '/home/ubuntu/rayca-sessions/5d647916-53bb-4128-a9c7-1207887f20a0-d11115b837f3/synthetic_schemes.html'

new_html = html[:orig_row_start] + new_row + html[orig_row_end:]

with open(path, 'w') as f:
    f.write(new_html)

size_kb = len(new_html) / 1024
print(f"Written: {size_kb:.1f} KB")

# Verify the fix
check_start = new_html.find('id="MCUF651"')
check_end   = new_html.find('<section ', check_start + 100)
chunk       = new_html[check_start:check_end]
chunk_clean = re.sub(r'data:image/svg\+xml;base64,[A-Za-z0-9+/=]+', 'B64', chunk)
text        = re.sub(r'<[^>]+>', ' ', chunk_clean)
text        = re.sub(r'\s+', ' ', text).strip()
print("\nMCUF651 Route 1 text after fix:")
print(text[:500])
