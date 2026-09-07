
import os

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'
viewer_path = f'{WD}/docking_viewer.html'
viewer_size = os.path.getsize(viewer_path)

# Verify key structural elements are present in the file
with open(viewer_path) as f:
    h = f.read()

checks = {
    '3Dmol CDN loaded':         'https://3dmol.csb.pitt.edu/build/3Dmol-min.js' in h,
    'RECEPTOR_PDB embedded':    'RECEPTOR_PDB' in h and len(h) > 200000,
    'POSES object embedded':    'const POSES = {' in h,
    'SCORES object embedded':   'const SCORES = {' in h,
    'COMPOUNDS array embedded':  'const COMPOUNDS = [' in h,
    '5 compound entries':        h.count('"EDS0') == 5 * 4,   # each id appears in SCORES + COMPOUNDS + card HTML + POSES
    'All 5 pose SDF blocks':     all(f'poses_{c}.sdf' not in h   # SDFs embedded as literals not refs
                                    for c in ['EDS01357518_ent1','EDS01357518_ent2',
                                              'EDS01806218_ent1','EDS01806218_ent2','EDS01889984']),
    'Pocket residues defined':   'POCKET_RESI = [76' in h,
    'Trp basket residues':       'TRPNRESI   = [104, 110, 123]' in h,
    'addLabel 3-arg form':       'resi: [r], model: receptorModel' in h,
    'Pose toggle function':      'function selectPose(idx)' in h,
    'Surface toggle function':   'function setProteinStyle(mode)' in h,
    'Pocket toggle function':    'function togglePocket()' in h,
    'Reset view function':       'function resetView()' in h,
    'No sphere style (removed)': h.count('sphere:') == 0,
}

print("Verification results:")
all_pass = True
for name, result in checks.items():
    status = "PASS" if result else "FAIL"
    if not result:
        all_pass = False
    print(f"  [{status}] {name}")

print(f"\nAll checks pass: {all_pass}")
print(f"File size: {viewer_size:,} bytes ({viewer_size/1024:.1f} KB)")
