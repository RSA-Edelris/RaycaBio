
# Verify each insertion point is unique
checks = {
    # 1. After CONTACTS block
    '1_contacts_end': h.count('\n};\n\n// ── State'),
    # 2. showCrystal state var
    '2_showCrystal': h.count('let showCrystal     = true;'),
    # 3. removeAllSurfaces in rebuildScene
    '3_removeAllSurfaces': h.count('viewer.removeAllSurfaces();'),
    # 4. end of rebuildScene
    '4_rebuildScene_end': h.count('viewer.zoomTo({model: poseModels[0]}, 1000);\n  viewer.render();\n}\n\n// ── Pocket'),
    # 5. after setProteinStyle function (to insert drawInteractions)
    '5_after_setProteinStyle': h.count('// ── Pocket residues style'),
    # 6. controls bar spacer
    '6_spacer': h.count('<div class="spacer"></div>\n\n    <button class="btn" onclick="resetView()">'),
}
for k, v in checks.items():
    print(f"{k}: {v} {'OK' if v == 1 else 'PROBLEM'}")
