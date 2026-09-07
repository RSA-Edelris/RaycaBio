
h2 = h

# ── Patch 1: Insert INTERACTIONS constant after CONTACTS block ─────────────
h2 = h2.replace(
    '\n};\n\n// ── State',
    '\n};\n\n' + interactions_js + '\n\n// ── State'
)

# ── Patch 2: Add showInteractions state variable ───────────────────────────
h2 = h2.replace(
    'let showCrystal     = true;',
    'let showCrystal     = true;\nlet showInteractions = true;'
)

# ── Patch 3: Add removeAllShapes() in rebuildScene ─────────────────────────
h2 = h2.replace(
    'viewer.removeAllSurfaces();',
    'viewer.removeAllSurfaces();\n  viewer.removeAllShapes();'
)

# ── Patch 4: Add drawInteractions call before final render in rebuildScene ──
h2 = h2.replace(
    'viewer.zoomTo({model: poseModels[0]}, 1000);\n  viewer.render();\n}\n\n// ── Pocket',
    'viewer.zoomTo({model: poseModels[0]}, 1000);\n  if (currentCompound && INTERACTIONS[currentCompound]) {\n    drawInteractions(INTERACTIONS[currentCompound]);\n  }\n  viewer.render();\n}\n\n// ── Pocket'
)

# ── Patch 5: Insert drawInteractions function after "// ── Pocket residues" ─
h2 = h2.replace(
    '// ── Pocket residues style',
    draw_fn + '\n// ── Pocket residues style'
)

# ── Patch 6: Add Interactions toggle button in controls bar ────────────────
h2 = h2.replace(
    '<div class="spacer"></div>\n\n    <button class="btn" onclick="resetView()">',
    '<div class="ctrl-group">\n      <span class="ctrl-label">Interactions</span>\n      <button class="btn active" id="btn-interactions" onclick="toggleInteractions()">H-bond / π</button>\n    </div>\n\n    <div class="spacer"></div>\n\n    <button class="btn" onclick="resetView()">'
)

# ── Verify patches ──────────────────────────────────────────────────────────
assert h2.count('const INTERACTIONS') == 1, "INTERACTIONS const missing"
assert h2.count('let showInteractions') == 1, "showInteractions state missing"
assert h2.count('viewer.removeAllShapes()') >= 1, "removeAllShapes missing"
assert h2.count('drawInteractions(') >= 2, "drawInteractions calls missing"
assert h2.count('function drawInteractions') == 1, "drawInteractions fn missing"
assert h2.count('btn-interactions') == 2, "btn-interactions button missing"
assert h2.count('toggleInteractions') == 2, "toggleInteractions missing"

print("All assertions passed")
print(f"Old size: {len(h):,}  New size: {len(h2):,}  Delta: +{len(h2)-len(h):,}")
