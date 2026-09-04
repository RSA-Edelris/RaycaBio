
# Get full structure of the row (strip base64) to understand exact HTML template
clean_row = re.sub(r'(src=")data:image/svg\+xml;base64,[A-Za-z0-9+/=]+(\")', r'\1B64\2', html[orig_row_start:orig_row_end])
# print first 2000 chars to see the mol-box and arrow structure
print(clean_row[:2500])
