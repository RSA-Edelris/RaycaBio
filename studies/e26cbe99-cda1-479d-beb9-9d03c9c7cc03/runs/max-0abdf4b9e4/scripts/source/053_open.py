
with open(f'{WD}/docking_viewer.html') as f:
    h = f.read()

# 1. Replace static POCKET_RESI / TRPNRESI with CONTACTS object
old_pocket = """// Pocket residues (chain B, resi from complex analysis)
const POCKET_RESI = [76, 77, 78, 80, 82, 101, 102, 103, 104, 110, 112, 120, 123, 125];
const TRPNRESI   = [104, 110, 123];  // tri-Trp basket"""

new_pocket = f"""// Per-compound contact residues (chain B, ≤4.0 Å from best pose)
const CONTACTS = {contacts_js};"""

assert old_pocket in h, "POCKET_RESI block not found"
h = h.replace(old_pocket, new_pocket)

# 2. Replace applyPocketStyle() — old takes no args, new takes contactData
old_fn = """// ── Pocket residues style ──────────────────────────────────────────────────
function applyPocketStyle() {
  if (!receptorModel) return;
  // Base sticks for all pocket residues
  viewer.setStyle(
    {model: receptorModel, resi: POCKET_RESI},
    {
      cartoon: { color: '#b0b8cc', opacity: 0.85, thickness: 0.4 },
      stick:   { colorscheme: 'Jmol', radius: 0.16, opacity: 0.9 }
    }
  );
  // Tryptophans slightly larger
  viewer.setStyle(
    {model: receptorModel, resi: TRPNRESI},
    {
      cartoon: { color: '#b0b8cc', opacity: 0.85, thickness: 0.4 },
      stick:   { colorscheme: 'Jmol', radius: 0.20, opacity: 1.0 },
    }
  );
  // Label the three TRPs (3-arg form: text, style, selection)
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
  });
}"""

new_fn = """// ── Pocket residues style (dynamic per-compound) ──────────────────────────
function applyPocketStyle(contactData) {
  if (!receptorModel || !contactData) return;
  const resiList = contactData.resi;
  const trpList  = contactData.trp;

  // All contacts as CPK sticks
  viewer.setStyle(
    {model: receptorModel, resi: resiList},
    {
      cartoon: { color: '#b0b8cc', opacity: 0.85, thickness: 0.4 },
      stick:   { colorscheme: 'Jmol', radius: 0.15, opacity: 0.9 }
    }
  );
  // TRP basket — slightly larger, full opacity
  if (trpList.length > 0) {
    viewer.setStyle(
      {model: receptorModel, resi: trpList},
      {
        cartoon: { color: '#b0b8cc', opacity: 0.85, thickness: 0.4 },
        stick:   { colorscheme: 'Jmol', radius: 0.20, opacity: 1.0 }
      }
    );
  }
  // Labels for all contacts
  contactData.labels.forEach(([resn, resi]) => {
    const isTrp = trpList.includes(resi);
    viewer.addLabel(`${resn} ${resi}`, {
      fontSize: isTrp ? 11 : 9,
      fontColor: isTrp ? '#fde68a' : '#cbd5e1',
      backgroundColor: '#00000099',
      backgroundOpacity: 0.6,
      showBackground: true,
      bold: isTrp,
      inFront: true,
    }, {resi: [resi], model: receptorModel, atom: 'CA'});
  });

  // Crystal-unique contacts (in lighter style when LVY ref is visible)
  if (showCrystal && CONTACTS.crystal_lvy) {
    const crystalOnly = CONTACTS.crystal_lvy.resi.filter(r => !resiList.includes(r));
    if (crystalOnly.length > 0) {
      viewer.setStyle(
        {model: receptorModel, resi: crystalOnly},
        {
          cartoon: { color: '#b0b8cc', opacity: 0.85, thickness: 0.4 },
          stick:   { colorscheme: 'Jmol', radius: 0.12, opacity: 0.55 }
        }
      );
      crystalOnly.forEach(r => {
        const entry = CONTACTS.crystal_lvy.labels.find(([n, ri]) => ri === r);
        if (entry) {
          viewer.addLabel(`${entry[0]} ${entry[1]}`, {
            fontSize: 8, fontColor: '#94a3b8',
            backgroundColor: '#00000088', backgroundOpacity: 0.55,
            showBackground: true, inFront: true,
          }, {resi: [r], model: receptorModel, atom: 'CA'});
        }
      });
    }
  }
}"""

assert old_fn in h, "applyPocketStyle() not found"
h = h.replace(old_fn, new_fn)

# 3. Update calls to applyPocketStyle() — add currentCompound arg
h = h.replace('if (showPocket) applyPocketStyle();',
              'if (showPocket) applyPocketStyle(CONTACTS[currentCompound]);')
h = h.replace(
    """  if (showPocket) {
    applyPocketStyle();
  } else {""",
    """  if (showPocket) {
    applyPocketStyle(CONTACTS[currentCompound]);
  } else {""")

# 4. In togglePocket() the "else" branch resets pocket residues — update resi list
old_toggle_else = """    viewer.setStyle(
      {model: receptorModel, resi: POCKET_RESI},
      {cartoon: { color: '#b0b8cc', opacity: 0.85, thickness: 0.4 }}
    );"""
new_toggle_else = """    const allResi = currentCompound
      ? [...new Set([
          ...(CONTACTS[currentCompound]?.resi || []),
          ...(showCrystal ? CONTACTS.crystal_lvy.resi : [])
        ])]
      : [];
    viewer.setStyle(
      {model: receptorModel, resi: allResi},
      {cartoon: { color: '#b0b8cc', opacity: 0.85, thickness: 0.4 }}
    );"""
h = h.replace(old_toggle_else, new_toggle_else)

# 5. After toggleCrystal re-enables crystal, refresh pocket to show crystal contacts
old_crystal_on = """    if (crystalModel === null) {
      crystalModel = viewer.addModel(CRYSTAL_LVY_PDB, 'pdb');
      viewer.setStyle({model: crystalModel}, {
        stick: { color: '#ffffff', radius: 0.12, opacity: 0.70 },
      });
    }
  } else {"""
new_crystal_on = """    if (crystalModel === null) {
      crystalModel = viewer.addModel(CRYSTAL_LVY_PDB, 'pdb');
      viewer.setStyle({model: crystalModel}, {
        stick: { color: '#ffffff', radius: 0.12, opacity: 0.70 },
      });
    }
    // Refresh pocket to include crystal-unique contacts
    if (showPocket && currentCompound) {
      viewer.removeAllLabels();
      applyPocketStyle(CONTACTS[currentCompound]);
    }
  } else {"""
h = h.replace(old_crystal_on, new_crystal_on)

# Also refresh pocket when crystal is hidden
old_crystal_off = """    if (crystalModel !== null) {
      viewer.removeModel(crystalModel);
      crystalModel = null;
    }
  }
  viewer.render();
}"""
new_crystal_off = """    if (crystalModel !== null) {
      viewer.removeModel(crystalModel);
      crystalModel = null;
    }
    // Remove crystal-unique contact sticks/labels
    if (showPocket && currentCompound) {
      viewer.removeAllLabels();
      applyPocketStyle(CONTACTS[currentCompound]);
    }
  }
  viewer.render();
}"""
h = h.replace(old_crystal_off, new_crystal_off)

# 6. Update sidebar legend
h = h.replace(
    '    <b style="color:#a5b4fc">Pocket residues shown:</b><br>\n    TRP 104 · TRP 110 · TRP 123<br>\n    ASN 76 · HIS 78 · TYR 80<br>',
    '    <b style="color:#a5b4fc">Contacts at ≤4.0 Å (best pose):</b><br>\n    TRP 336 · TRP 342 · TRP 356<br>\n    per-compound · gold labels<br>'
)

with open(f'{WD}/docking_viewer.html', 'w') as f:
    f.write(h)

import os
size = os.path.getsize(f'{WD}/docking_viewer.html')

# Sanity checks
assert 'const CONTACTS = ' in h
assert 'function applyPocketStyle(contactData)' in h
assert 'CONTACTS[currentCompound]' in h
assert 'crystal_lvy' in h
assert 'POCKET_RESI' not in h, "old POCKET_RESI still present"
assert 'TRPNRESI' not in h,   "old TRPNRESI still present"
print(f"Updated: {size:,} bytes ({size/1024:.0f} KB)")
print("All assertions passed")
