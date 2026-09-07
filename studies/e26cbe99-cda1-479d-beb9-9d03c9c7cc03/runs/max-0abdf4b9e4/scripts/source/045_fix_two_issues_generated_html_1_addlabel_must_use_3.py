
# Fix two issues in the generated HTML:
# 1. addLabel must use 3-argument form for selection-based positioning
# 2. Remove sphere style (overcomplicates for small mol sticks)
# 3. Minor: inactive poses use opacity:0 sphere is needless — strip it

with open(f'{WD}/docking_viewer.html') as f:
    h = f.read()

# Fix 1: replace the label block
old_label = """  // Label the three TRPs
  TRPNRESI.forEach(r => {
    viewer.addLabel(`TRP ${r}`, {
      position: { resi: r, model: receptorModel },
      fontSize: 10,
      fontColor: '#fde68a',
      backgroundColor: 'rgba(0,0,0,0.55)',
      backgroundOpacity: 0.55,
      showBackground: true,
      bold: true,
      alignment: 'bottomCenter',
    });
  });"""

new_label = """  // Label the three TRPs (3-arg form: text, style, selection)
  TRPNRESI.forEach(r => {
    viewer.addLabel(`TRP ${r}`, {
      fontSize: 10,
      fontColor: '#fde68a',
      backgroundColor: '#00000099',
      backgroundOpacity: 0.6,
      showBackground: true,
      bold: true,
      inFront: true,
    }, {resi: [r], model: receptorModel, atom: 'CA'});
  });"""

h = h.replace(old_label, new_label)

# Fix 2: strip sphere style from setStyle calls (sticks are sufficient)
old_sphere_active = """      sphere: {
        color: color,
        radius: isActive ? 0.3 : 0.0,
        opacity: isActive ? 0.85 : 0.0,
      }"""
h = h.replace(old_sphere_active, '')

# Fix the trailing commas left after sphere removal
import re
h = re.sub(r',\s*\}(\s*\}\);)', r'\n      }$1', h)

with open(f'{WD}/docking_viewer.html', 'w') as f:
    f.write(h)

import os
size = os.path.getsize(f'{WD}/docking_viewer.html')
print(f"Updated: {size:,} bytes ({size/1024:.0f} KB)")

# Quick sanity checks
assert 'addLabel(`TRP ${r}`, {' in h, "label fix missing"
assert 'resi: [r], model: receptorModel' in h, "label selection missing"
assert h.count('sphere:') == 0, f"sphere style still present ({h.count('sphere:')} times)"
print("Sanity checks passed")
