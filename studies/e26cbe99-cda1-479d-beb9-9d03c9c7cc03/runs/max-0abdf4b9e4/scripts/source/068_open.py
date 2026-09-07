
with open(f'{WD}/docking_viewer.html', 'w') as f:
    f.write(h2)

import os
sz = os.path.getsize(f'{WD}/docking_viewer.html')
print(f"Written: {sz:,} bytes ({sz//1024} KB)")

# Quick spot checks on the saved file
with open(f'{WD}/docking_viewer.html') as f:
    h_check = f.read()

checks = {
    'INTERACTIONS const':           h_check.count('const INTERACTIONS') == 1,
    'showInteractions state':       h_check.count('let showInteractions') == 1,
    'removeAllShapes':              h_check.count('viewer.removeAllShapes()') >= 1,
    'drawInteractions fn defined':  h_check.count('function drawInteractions') == 1,
    'drawInteractions called':      h_check.count('drawInteractions(') >= 2,
    'toggleInteractions fn':        h_check.count('function toggleInteractions') == 1,
    'btn-interactions button':      h_check.count('id="btn-interactions"') == 1,
    'H-bond hbonds key':            h_check.count('"hbonds"') >= 6,
    'pistack key':                  h_check.count('"pistack"') >= 6,
    'crystal_lvy in INTERACTIONS':  h_check.count('"crystal_lvy"') >= 2,
    'dashed cyan addLine':          h_check.count("color: '#06b6d4'") >= 1,
    'purple cylinder':              h_check.count("color: '#c026d3'") >= 1,
}
for k, v in checks.items():
    print(f"  {'PASS' if v else 'FAIL'}: {k}")
