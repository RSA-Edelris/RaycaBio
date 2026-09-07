
def js_str(s):
    return s.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

# Rebuild receptor_js and poses_js since js_str was dropped
with open(f'{WD}/PB-20260903-4CI2_receptor_trimmed_fixed.pdb') as f:
    receptor_pdb = f.read()
receptor_js = js_str(receptor_pdb)

poses_js_parts = []
for (cid, *_) in compounds:
    with open(f'{WD}/poses_{cid}.sdf') as f:
        content = f.read()
    blocks = [b.strip() + '\n$$$$' for b in content.split('$$$$') if b.strip()]
    blocks_js = ',\n'.join(f'`{js_str(b)}`' for b in blocks)
    poses_js_parts.append(f'  "{cid}": [{blocks_js}]')
poses_js = '{\n' + ',\n'.join(poses_js_parts) + '\n}'

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CRBN Docking Viewer — 4CI2</title>
<script src="https://3dmol.csb.pitt.edu/build/3Dmol-min.js"></script>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --bg: #0f0f1a;
  --panel: #1a1a2e;
  --panel2: #16213e;
  --border: #2a2a4a;
  --text: #e2e8f0;
  --sub: #94a3b8;
  --accent: #6366f1;
}}

body {{
  display: flex; height: 100vh; overflow: hidden;
  background: var(--bg); color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
  font-size: 13px;
}}

/* ── Sidebar ─────────────────────────────────────────────────── */
#sidebar {{
  width: 270px; min-width: 270px;
  background: var(--panel);
  border-right: 1px solid var(--border);
  display: flex; flex-direction: column;
  overflow-y: auto;
}}

#sidebar-header {{
  padding: 16px 14px 12px;
  border-bottom: 1px solid var(--border);
}}
#sidebar-header h1 {{
  font-size: 14px; font-weight: 600; letter-spacing: 0.02em;
  color: #a5b4fc;
}}
#sidebar-header p {{
  margin-top: 3px; font-size: 11px; color: var(--sub);
}}

.section-label {{
  padding: 10px 14px 4px;
  font-size: 10px; font-weight: 600; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--sub);
}}

/* ── Compound cards ──────────────────────────────────────────── */
.compound-card {{
  margin: 4px 8px;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid var(--border);
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
  background: var(--panel2);
}}
.compound-card:hover {{
  border-color: #4a4a7a;
  background: #1e2040;
}}
.compound-card.active {{
  border-color: var(--card-color, #6366f1);
  background: color-mix(in srgb, var(--card-color, #6366f1) 12%, var(--panel2));
}}

.card-header {{
  display: flex; align-items: center; gap: 8px; margin-bottom: 7px;
}}
.color-dot {{
  width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0;
}}
.card-name {{
  font-size: 12px; font-weight: 600; white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis; flex: 1;
}}
.stereo-badge {{
  font-size: 10px; color: var(--sub); flex-shrink: 0;
}}
.best-badge {{
  font-size: 9px; font-weight: 700; letter-spacing: 0.04em;
  background: #10b981; color: #fff;
  padding: 1px 5px; border-radius: 4px; flex-shrink: 0;
}}

.score-grid {{
  display: grid; grid-template-columns: 1fr 1fr 1fr;
  gap: 4px;
}}
.score-cell {{
  background: rgba(0,0,0,0.25);
  border-radius: 5px;
  padding: 4px 5px;
  text-align: center;
}}
.score-label {{ font-size: 9px; color: var(--sub); margin-bottom: 2px; }}
.score-val {{
  font-size: 12px; font-weight: 600; font-variant-numeric: tabular-nums;
}}
.score-val.neg {{ color: #34d399; }}
.score-val.pos {{ color: #f87171; }}
.score-val.mid {{ color: #93c5fd; }}

/* ── Main viewer area ────────────────────────────────────────── */
#main {{
  flex: 1; display: flex; flex-direction: column; min-width: 0;
}}

#viewer-wrap {{
  flex: 1; position: relative; overflow: hidden;
}}
#viewer {{
  position: absolute; inset: 0;
}}

/* ── Controls bar ────────────────────────────────────────────── */
#controls {{
  background: var(--panel);
  border-top: 1px solid var(--border);
  padding: 8px 14px;
  display: flex; align-items: center; gap: 16px; flex-wrap: wrap;
}}

.ctrl-group {{
  display: flex; align-items: center; gap: 6px;
}}
.ctrl-label {{
  font-size: 10px; font-weight: 600; letter-spacing: 0.06em;
  text-transform: uppercase; color: var(--sub);
}}

.btn {{
  padding: 4px 10px; font-size: 12px; font-weight: 500;
  border-radius: 5px; border: 1px solid var(--border);
  background: var(--panel2); color: var(--text);
  cursor: pointer; transition: all 0.12s;
  font-family: inherit;
}}
.btn:hover {{ background: #1e2040; border-color: #4a4a7a; }}
.btn.active {{
  background: var(--accent); border-color: var(--accent);
  color: #fff;
}}
.btn.pose-btn {{ min-width: 30px; text-align: center; padding: 4px 6px; }}

#pose-label {{
  font-size: 11px; color: var(--sub);
}}

.spacer {{ flex: 1; }}

#info-bar {{
  font-size: 11px; color: var(--sub);
  white-space: nowrap;
}}
</style>
</head>
<body>

<!-- ── Sidebar ─────────────────────────────────────── -->
<div id="sidebar">
  <div id="sidebar-header">
    <h1>CRBN Docking Viewer</h1>
    <p>PDB 4CI2 &nbsp;·&nbsp; 5 compounds &nbsp;·&nbsp; 5 poses each</p>
  </div>

  <div class="section-label">Compounds</div>
  <div id="card-list"></div>

  <div style="flex:1"></div>
  <div style="padding:10px 14px 14px; border-top:1px solid var(--border); font-size:10px; color:var(--sub); line-height:1.6;">
    <b style="color:#a5b4fc">Pocket residues shown:</b><br>
    TRP 104 · TRP 110 · TRP 123<br>
    ASN 76 · HIS 78 · TYR 80<br><br>
    ΔG = −1.364 × pKi (CNN-derived)
  </div>
</div>

<!-- ── Main ────────────────────────────────────────── -->
<div id="main">
  <div id="viewer-wrap">
    <div id="viewer"></div>
  </div>

  <div id="controls">
    <div class="ctrl-group">
      <span class="ctrl-label">Pose</span>
      <div id="pose-btns">
        <button class="btn pose-btn active" onclick="selectPose(0)">1</button>
        <button class="btn pose-btn" onclick="selectPose(1)">2</button>
        <button class="btn pose-btn" onclick="selectPose(2)">3</button>
        <button class="btn pose-btn" onclick="selectPose(3)">4</button>
        <button class="btn pose-btn" onclick="selectPose(4)">5</button>
      </div>
    </div>

    <div class="ctrl-group">
      <span class="ctrl-label">Protein</span>
      <button class="btn active" id="btn-cartoon" onclick="setProteinStyle('cartoon')">Cartoon</button>
      <button class="btn" id="btn-surface" onclick="setProteinStyle('surface')">+ Surface</button>
    </div>

    <div class="ctrl-group">
      <span class="ctrl-label">Pocket</span>
      <button class="btn active" id="btn-pocket" onclick="togglePocket()">Residues</button>
    </div>

    <div class="spacer"></div>

    <button class="btn" onclick="resetView()">⟳ Reset view</button>
    <div id="info-bar">Select a compound</div>
  </div>
</div>

<script>
// ── Embedded data ──────────────────────────────────────────────────────────
const RECEPTOR_PDB = `{receptor_js}`;

const POSES = {poses_js};

const SCORES = {scores_js};

const COMPOUNDS = {compounds_js};

// Pocket residues (chain B, resi from complex analysis)
const POCKET_RESI = [76, 77, 78, 80, 82, 101, 102, 103, 104, 110, 112, 120, 123, 125];
const TRPNRESI   = [104, 110, 123];  // tri-Trp basket

// ── State ──────────────────────────────────────────────────────────────────
let viewer;
let currentCompound = null;
let currentPose     = 0;
let proteinStyle    = 'cartoon';   // 'cartoon' | 'surface'
let showPocket      = true;
let poseModels      = [];
let receptorModel   = null;
let surfaceID       = null;

// ── Init viewer ────────────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {{
  const el = document.getElementById('viewer');
  viewer = $3Dmol.createViewer(el, {{
    backgroundColor: '#0f0f1a',
    antialias: true,
    defaultcolors: $3Dmol.elementColors.Jmol,
  }});

  buildCards();
  loadCompound(COMPOUNDS[3].id);  // default: best compound (1S,2S)
}});

// ── Build sidebar cards ────────────────────────────────────────────────────
function buildCards() {{
  const list = document.getElementById('card-list');
  COMPOUNDS.forEach(c => {{
    const s = SCORES[c.id];
    const isBest = c.id === 'EDS01806218_ent2';
    const div = document.createElement('div');
    div.className = 'compound-card';
    div.id = 'card-' + c.id;
    div.style.setProperty('--card-color', c.color);
    div.innerHTML = `
      <div class="card-header">
        <span class="color-dot" style="background:${{c.color}}"></span>
        <span class="card-name">${{c.parent}}</span>
        <span class="stereo-badge">${{c.stereo}}</span>
        ${{isBest ? '<span class="best-badge">BEST</span>' : ''}}
      </div>
      <div class="score-grid">
        <div class="score-cell">
          <div class="score-label">Vina</div>
          <div class="score-val neg">${{s.vina.toFixed(2)}}</div>
        </div>
        <div class="score-cell">
          <div class="score-label">CNN</div>
          <div class="score-val mid">${{s.cnn_pose.toFixed(3)}}</div>
        </div>
        <div class="score-cell">
          <div class="score-label">ΔG kcal/mol</div>
          <div class="score-val neg">${{s.dG.toFixed(2)}}</div>
        </div>
      </div>`;
    div.addEventListener('click', () => loadCompound(c.id));
    list.appendChild(div);
  }});
}}

// ── Load compound ──────────────────────────────────────────────────────────
function loadCompound(cid) {{
  currentCompound = cid;
  currentPose     = 0;

  // Update card highlight
  document.querySelectorAll('.compound-card').forEach(el => el.classList.remove('active'));
  const card = document.getElementById('card-' + cid);
  if (card) card.classList.add('active');

  // Update pose buttons
  document.querySelectorAll('.pose-btn').forEach((b, i) => {{
    b.classList.toggle('active', i === 0);
  }});

  rebuildScene();

  const c = COMPOUNDS.find(x => x.id === cid);
  const s = SCORES[cid];
  document.getElementById('info-bar').textContent =
    `${{c.parent}} ${{c.stereo}}  ·  Vina ${{s.vina.toFixed(2)}} kcal/mol  ·  ΔG ${{s.dG.toFixed(2)}} kcal/mol`;
}}

// ── Rebuild 3D scene ───────────────────────────────────────────────────────
function rebuildScene() {{
  viewer.removeAllModels();
  viewer.removeAllSurfaces();
  surfaceID    = null;
  poseModels   = [];
  receptorModel = null;

  const c    = COMPOUNDS.find(x => x.id === currentCompound);
  const color = c ? c.color : '#aaaaaa';

  // Receptor
  receptorModel = viewer.addModel(RECEPTOR_PDB, 'pdb');
  viewer.setStyle({{model: receptorModel}}, {{
    cartoon: {{ color: '#b0b8cc', opacity: 0.85, thickness: 0.4, arrows: true }}
  }});

  // Pocket residues as sticks
  if (showPocket) applyPocketStyle();

  // All 5 poses
  const psdfs = POSES[currentCompound];
  psdfs.forEach((sdf, i) => {{
    const m = viewer.addModel(sdf, 'sdf');
    poseModels.push(m);
    const isActive = (i === currentPose);
    viewer.setStyle({{model: m}}, {{
      stick: {{
        colorscheme: 'default',
        color: color,
        radius: isActive ? 0.18 : 0.10,
        opacity: isActive ? 1.0 : 0.15,
      }},
      sphere: {{
        color: color,
        radius: isActive ? 0.3 : 0.0,
        opacity: isActive ? 0.85 : 0.0,
      }}
    }});
  }});

  // Surface if requested
  if (proteinStyle === 'surface') {{
    surfaceID = viewer.addSurface(
      $3Dmol.SurfaceType.VDW,
      {{ opacity: 0.35, colorscheme: 'whiteCarbon' }},
      {{ model: receptorModel }}
    );
  }}

  viewer.zoomTo({{model: poseModels[0]}}, 1000);
  viewer.render();
}}

// ── Pocket residues style ──────────────────────────────────────────────────
function applyPocketStyle() {{
  if (!receptorModel) return;
  // Base sticks for all pocket residues
  viewer.setStyle(
    {{model: receptorModel, resi: POCKET_RESI}},
    {{
      cartoon: {{ color: '#b0b8cc', opacity: 0.85, thickness: 0.4 }},
      stick:   {{ colorscheme: 'Jmol', radius: 0.16, opacity: 0.9 }}
    }}
  );
  // Tryptophans slightly larger
  viewer.setStyle(
    {{model: receptorModel, resi: TRPNRESI}},
    {{
      cartoon: {{ color: '#b0b8cc', opacity: 0.85, thickness: 0.4 }},
      stick:   {{ colorscheme: 'Jmol', radius: 0.20, opacity: 1.0 }},
    }}
  );
  // Label the three TRPs
  TRPNRESI.forEach(r => {{
    viewer.addLabel(`TRP ${{r}}`, {{
      position: {{ resi: r, model: receptorModel }},
      fontSize: 10,
      fontColor: '#fde68a',
      backgroundColor: 'rgba(0,0,0,0.55)',
      backgroundOpacity: 0.55,
      showBackground: true,
      bold: true,
      alignment: 'bottomCenter',
    }});
  }});
}}

// ── Select pose ────────────────────────────────────────────────────────────
function selectPose(idx) {{
  currentPose = idx;
  document.querySelectorAll('.pose-btn').forEach((b, i) => {{
    b.classList.toggle('active', i === idx);
  }});

  const c     = COMPOUNDS.find(x => x.id === currentCompound);
  const color  = c ? c.color : '#aaaaaa';

  poseModels.forEach((m, i) => {{
    const isActive = (i === idx);
    viewer.setStyle({{model: m}}, {{
      stick: {{
        colorscheme: 'default',
        color: color,
        radius: isActive ? 0.18 : 0.10,
        opacity: isActive ? 1.0 : 0.15,
      }},
      sphere: {{
        color: color,
        radius: isActive ? 0.3 : 0.0,
        opacity: isActive ? 0.85 : 0.0,
      }}
    }});
  }});

  viewer.zoomTo({{model: poseModels[idx]}}, 500);
  viewer.render();
}}

// ── Protein display style ──────────────────────────────────────────────────
function setProteinStyle(mode) {{
  proteinStyle = mode;
  document.getElementById('btn-cartoon').classList.toggle('active', mode === 'cartoon');
  document.getElementById('btn-surface').classList.toggle('active', mode === 'surface');

  if (mode === 'surface') {{
    if (surfaceID === null && receptorModel) {{
      surfaceID = viewer.addSurface(
        $3Dmol.SurfaceType.VDW,
        {{ opacity: 0.35, colorscheme: 'whiteCarbon' }},
        {{ model: receptorModel }}
      );
    }}
  }} else {{
    if (surfaceID !== null) {{
      viewer.removeSurface(surfaceID);
      surfaceID = null;
    }}
  }}
  viewer.render();
}}

// ── Toggle pocket residues ─────────────────────────────────────────────────
function togglePocket() {{
  showPocket = !showPocket;
  document.getElementById('btn-pocket').classList.toggle('active', showPocket);
  viewer.removeAllLabels();

  if (!receptorModel) return;

  if (showPocket) {{
    applyPocketStyle();
  }} else {{
    viewer.setStyle(
      {{model: receptorModel, resi: POCKET_RESI}},
      {{cartoon: {{ color: '#b0b8cc', opacity: 0.85, thickness: 0.4 }}}}
    );
  }}
  viewer.render();
}}

// ── Reset view ─────────────────────────────────────────────────────────────
function resetView() {{
  if (poseModels.length > 0) {{
    viewer.zoomTo({{model: poseModels[currentPose]}}, 600);
    viewer.render();
  }}
}}
</script>
</body>
</html>"""

out_path = f'{WD}/docking_viewer.html'
with open(out_path, 'w') as f:
    f.write(html)

import os
size = os.path.getsize(out_path)
print(f"Written: {out_path}")
print(f"Size: {size:,} bytes ({size/1024:.0f} KB)")
