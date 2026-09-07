
def js_str(s):
    return s.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

lvy_js = js_str(lvy_pdb)

with open(f'{WD}/docking_viewer.html') as f:
    h = f.read()

# 1. Embed crystal data after COMPOUNDS constant
crystal_data = f'\nconst CRYSTAL_LVY_PDB = `{lvy_js}`;\n'
h = h.replace(
    'const COMPOUNDS = ',
    'const CRYSTAL_LVY_PDB = `' + lvy_js + '`;\n\nconst COMPOUNDS = '
)

# 2. Add crystalModel state variable alongside other state vars
h = h.replace(
    'let poseModels      = [];\nlet receptorModel   = null;\nlet surfaceID       = null;',
    'let poseModels      = [];\nlet receptorModel   = null;\nlet surfaceID       = null;\nlet crystalModel    = null;\nlet showCrystal     = true;'
)

# 3. In rebuildScene(), reset crystalModel and reload if showCrystal
h = h.replace(
    '  poseModels   = [];\n  receptorModel = null;',
    '  poseModels    = [];\n  receptorModel  = null;\n  crystalModel   = null;'
)

# After the surface block in rebuildScene, add crystal loading
old_surface_block = """  if (proteinStyle === 'surface') {
    surfaceID = viewer.addSurface(
      $3Dmol.SurfaceType.VDW,
      { opacity: 0.35, colorscheme: 'whiteCarbon' },
      { model: receptorModel }
    );
  }

  viewer.zoomTo"""

new_surface_block = """  if (proteinStyle === 'surface') {
    surfaceID = viewer.addSurface(
      $3Dmol.SurfaceType.VDW,
      { opacity: 0.35, colorscheme: 'whiteCarbon' },
      { model: receptorModel }
    );
  }

  // Crystal reference ligand
  if (showCrystal) {
    crystalModel = viewer.addModel(CRYSTAL_LVY_PDB, 'pdb');
    viewer.setStyle({model: crystalModel}, {
      stick: { color: '#ffffff', radius: 0.12, opacity: 0.70 },
    });
  }

  viewer.zoomTo"""

h = h.replace(old_surface_block, new_surface_block)

# 4. Add Crystal toggle button in controls bar after the Pocket group
h = h.replace(
    """    <div class="ctrl-group">
      <span class="ctrl-label">Pocket</span>
      <button class="btn active" id="btn-pocket" onclick="togglePocket()">Residues</button>
    </div>""",
    """    <div class="ctrl-group">
      <span class="ctrl-label">Pocket</span>
      <button class="btn active" id="btn-pocket" onclick="togglePocket()">Residues</button>
    </div>

    <div class="ctrl-group">
      <span class="ctrl-label">Crystal</span>
      <button class="btn active" id="btn-crystal" onclick="toggleCrystal()">LVY ref</button>
    </div>"""
)

# 5. Add toggleCrystal() function before resetView
h = h.replace(
    '// ── Reset view',
    """// ── Toggle crystal ligand ──────────────────────────────────────────────────
function toggleCrystal() {
  showCrystal = !showCrystal;
  document.getElementById('btn-crystal').classList.toggle('active', showCrystal);

  if (showCrystal) {
    if (crystalModel === null) {
      crystalModel = viewer.addModel(CRYSTAL_LVY_PDB, 'pdb');
      viewer.setStyle({model: crystalModel}, {
        stick: { color: '#ffffff', radius: 0.12, opacity: 0.70 },
      });
    }
  } else {
    if (crystalModel !== null) {
      viewer.removeModel(crystalModel);
      crystalModel = null;
    }
  }
  viewer.render();
}

// ── Reset view"""
)

# 6. Update sidebar legend note to mention crystal ref
h = h.replace(
    '    ΔG = −1.364 × pKi (CNN-derived)',
    '    <b style="color:#ffffff">White sticks</b> = LVY crystal ref<br>\n    ΔG = −1.364 × pKi (CNN-derived)'
)

with open(f'{WD}/docking_viewer.html', 'w') as f:
    f.write(h)

import os
size = os.path.getsize(f'{WD}/docking_viewer.html')

# Verify
assert 'CRYSTAL_LVY_PDB' in h
assert 'toggleCrystal()' in h
assert 'btn-crystal' in h
assert 'crystalModel' in h
assert 'LVY ref' in h
print(f"Updated: {size:,} bytes ({size/1024:.0f} KB)")
print("All assertions passed")
