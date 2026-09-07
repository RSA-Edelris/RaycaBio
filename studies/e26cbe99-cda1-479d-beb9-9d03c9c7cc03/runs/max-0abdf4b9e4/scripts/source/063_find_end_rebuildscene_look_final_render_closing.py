
# Find the end of rebuildScene - look for the final render() and closing brace
rebuild_pos = h.find('function rebuildScene()')
# Find all viewer.render() after rebuild_pos
pos = rebuild_pos
render_positions = []
while True:
    p = h.find('viewer.render()', pos)
    if p == -1 or p > rebuild_pos + 5000: break
    render_positions.append(p)
    pos = p + 1
print("viewer.render() positions in rebuildScene:", render_positions)
# Show context around last render() in rebuildScene
if render_positions:
    last_r = render_positions[-1]
    print(repr(h[last_r-100:last_r+200]))

# Find the controls bar - look for btn-crystal button area
btn_crystal_pos = h.find('btn-crystal')
print("\n== btn-crystal area ==")
print(h[btn_crystal_pos-100:btn_crystal_pos+400])
