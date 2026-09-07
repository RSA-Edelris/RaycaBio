
def js_str(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('`', '\\`')
    s = s.replace('${', '\\${')
    return s

def fmt_vec(v):
    return '{x:' + str(v[0]) + ',y:' + str(v[1]) + ',z:' + str(v[2]) + '}'

lines = ['const INTERACTIONS = {']
for cid, data in interactions.items():
    lines.append(f'  "{cid}": {{')
    lines.append('    "hbonds": [')
    for hb in data['hbonds']:
        label_js = js_str(hb['label'])
        s = fmt_vec(hb['start'])
        e = fmt_vec(hb['end'])
        lines.append(f'      {{start:{s}, end:{e}, label:"{label_js}"}},')
    lines.append('    ],')
    lines.append('    "pistack": [')
    for ps in data['pistack']:
        label_js = js_str(ps['label'])
        s = fmt_vec(ps['start'])
        e = fmt_vec(ps['end'])
        lines.append(f'      {{start:{s}, end:{e}, label:"{label_js}"}},')
    lines.append('    ]')
    lines.append('  },')
lines.append('};')
interactions_js = '\n'.join(lines)

# ── The drawInteractions function ─────────────────────────────────────────
draw_fn = r"""
// ── Draw interaction lines ────────────────────────────────────────────────
function drawInteractions(data) {
  viewer.removeAllShapes();
  if (!showInteractions || !data) return;

  // H-bonds: dashed cyan lines
  (data.hbonds || []).forEach(hb => {
    viewer.addLine({
      start: hb.start, end: hb.end,
      color: '#06b6d4', dashed: true, linewidth: 2
    });
    const mid = {
      x: (hb.start.x + hb.end.x) / 2,
      y: (hb.start.y + hb.end.y) / 2,
      z: (hb.start.z + hb.end.z) / 2
    };
    const d = Math.sqrt(
      Math.pow(hb.end.x - hb.start.x, 2) +
      Math.pow(hb.end.y - hb.start.y, 2) +
      Math.pow(hb.end.z - hb.start.z, 2)
    ).toFixed(1);
    viewer.addLabel(hb.label + ' ' + d + 'Å', {
      position: mid, fontSize: 9, fontColor: '#06b6d4',
      backgroundColor: 'transparent', showBackground: false,
      alignment: 'center'
    });
  });

  // pi-stacking: solid purple cylinders
  (data.pistack || []).forEach(ps => {
    viewer.addCylinder({
      start: ps.start, end: ps.end,
      radius: 0.12, color: '#c026d3', opacity: 0.8,
      dashed: false, fromCap: 1, toCap: 1
    });
    const mid = {
      x: (ps.start.x + ps.end.x) / 2,
      y: (ps.start.y + ps.end.y) / 2,
      z: (ps.start.z + ps.end.z) / 2
    };
    viewer.addLabel(ps.label, {
      position: mid, fontSize: 9, fontColor: '#c026d3',
      backgroundColor: 'transparent', showBackground: false,
      alignment: 'center'
    });
  });

  viewer.render();
}

function toggleInteractions() {
  showInteractions = !showInteractions;
  document.getElementById('btn-interactions').classList.toggle('active', showInteractions);
  drawInteractions(currentCompound ? INTERACTIONS[currentCompound] : null);
}
"""

print("draw_fn length:", len(draw_fn))
print(draw_fn[:300])
