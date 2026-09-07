
# Find the actual btn-crystal button in HTML (not in comment)
# Search for onclick="toggleCrystal"
toggle_pos = h.find('onclick="toggleCrystal()"')
print("== toggleCrystal button ==")
print(h[toggle_pos-200:toggle_pos+300])

# Find end of rebuildScene more precisely - look for pattern "viewer.render();\n}"
# after rebuildScene start
rebuild_pos = h.find('function rebuildScene()')
chunk = h[rebuild_pos:rebuild_pos+8000]
# find "viewer.render();\n}" in the chunk
rend_end = chunk.find('viewer.render();\n}')
if rend_end == -1:
    rend_end = chunk.find('viewer.render();\r\n}')
print(f"\nEnd of rebuildScene render at offset {rend_end} from function start")
print(repr(chunk[rend_end-100:rend_end+50]))
