
with open(f'{WD}/docking_viewer.html') as f:
    h = f.read()

# Find CONTACTS end, state variables, rebuildScene start, controls bar
contacts_end = h.find('const CONTACTS')
contacts_end2 = h.find('\n};', contacts_end) + 3  # end of CONTACTS block
print("== After CONTACTS block ==")
print(repr(h[contacts_end2:contacts_end2+200]))

# Find showCrystal state var area
show_pos = h.find('let showCrystal')
print("\n== showCrystal state var ==")
print(repr(h[show_pos-20:show_pos+200]))

# Find rebuildScene start
rebuild_pos = h.find('function rebuildScene()')
print("\n== rebuildScene start ==")
print(h[rebuild_pos:rebuild_pos+400])

# Find removeAllLabels in rebuildScene
ral_pos = h.find('viewer.removeAllLabels', rebuild_pos)
print("\n== removeAllLabels area ==")
print(h[ral_pos-20:ral_pos+200])

# Find where viewer.render() is called at end of rebuildScene (near drawInteractions insertion point)
# Find the 'applyPocketStyle' call
aps_pos = h.find('applyPocketStyle(', rebuild_pos)
print("\n== applyPocketStyle area ==")
print(h[aps_pos-10:aps_pos+200])
