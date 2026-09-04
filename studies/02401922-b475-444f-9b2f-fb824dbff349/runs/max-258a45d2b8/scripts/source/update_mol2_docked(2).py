#!/usr/bin/env python3
"""
Place antechamber mol2 at Vina docked pose coordinates.
Method: match mol2 heavy atoms to original SDF by XYZ proximity (antechamber
preserves coordinates), then map SDF→PDBQT by index (obabel preserves order),
then Kabsch rigid fit mol2→docked, apply to all 73 atoms.
"""
import sys, re
import numpy as np
from scipy.spatial.distance import cdist

def parse_mol2(path):
    lines = open(path).readlines()
    in_atom = False
    atoms = []
    atom_line_idx = []
    for i, line in enumerate(lines):
        s = line.strip()
        if s == '@<TRIPOS>ATOM': in_atom = True; continue
        if in_atom and s.startswith('@'): in_atom = False
        if in_atom and s:
            p = line.split()
            if len(p) >= 6:
                atype = p[5].lower()
                is_h = atype.startswith('h')
                atoms.append({'idx': len(atoms), 'line': i, 'name': p[1],
                               'x': float(p[2]), 'y': float(p[3]), 'z': float(p[4]),
                               'rest': line.split(None, 5)[5].rstrip() if len(p) > 5 else '',
                               'is_h': is_h, 'raw': line})
    return lines, atoms

def parse_sdf_heavy(path):
    """Return (N,3) array of heavy atom XYZ in SDF order."""
    lines = open(path).readlines()
    n = int(lines[3][:3])
    pts = []
    for i in range(4, 4+n):
        p = lines[i].split()
        if len(p) >= 4 and p[3] != 'H':
            pts.append([float(p[0]), float(p[1]), float(p[2])])
    return np.array(pts)

def parse_pdbqt_first_heavy(path):
    """Return (N,3) in SDF/obabel ordering (HD = polar H, skip)."""
    coords = []
    seen = False
    for line in open(path):
        if line.startswith('MODEL'):
            if seen: break
            seen = True; continue
        if line.startswith('ENDMDL'): break
        if line[:4] in ('ATOM','HEAT') or line.startswith('ATOM') or line.startswith('HETATM'):
            ad = line[77:79].strip()
            if ad == 'HD': continue
            coords.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return np.array(coords)

def kabsch(ref, mob):
    """Return R,t such that R@mob[i]+t ≈ ref[i]."""
    cr, cm = ref.mean(0), mob.mean(0)
    A = (ref-cr).T @ (mob-cm)
    U,S,Vt = np.linalg.svd(A)
    d = np.linalg.det(U@Vt)
    R = U @ np.diag([1,1,d]) @ Vt
    t = cr - R@cm
    return R, t

def update_mol2_docked(mol2_in, sdf_orig, pdbqt_docked, mol2_out):
    lines, atoms = parse_mol2(mol2_in)
    sdf_xyz   = parse_sdf_heavy(sdf_orig)
    pdbqt_xyz = parse_pdbqt_first_heavy(pdbqt_docked)

    assert len(sdf_xyz) == len(pdbqt_xyz), \
        f"SDF {len(sdf_xyz)} vs PDBQT {len(pdbqt_xyz)} heavy atom mismatch"

    # Map mol2 heavy → SDF index by XYZ proximity
    heavy = [a for a in atoms if not a['is_h']]
    mol2_xyz = np.array([[a['x'],a['y'],a['z']] for a in heavy])
    D = cdist(mol2_xyz, sdf_xyz)
    mol2_to_sdf = D.argmin(axis=1)
    assert (D.min(axis=1) < 0.01).all(), "mol2↔SDF coord mismatch >0.01Å"

    # Build paired arrays: mol2 heavy (reference, original) → pdbqt (target, docked)
    mob = mol2_xyz
    ref = np.array([pdbqt_xyz[mol2_to_sdf[i]] for i in range(len(heavy))])

    R, t = kabsch(ref, mob)  # fits mob onto ref

    # Apply to all atoms
    for a in atoms:
        orig = np.array([a['x'],a['y'],a['z']])
        new = R @ orig + t
        a['x'], a['y'], a['z'] = new

    # Verify RMSD on heavy atoms
    new_heavy = np.array([[a['x'],a['y'],a['z']] for a in atoms if not a['is_h']])
    rmsd = float(np.sqrt(np.mean(np.sum((ref - new_heavy)**2, axis=1))))

    # Write updated mol2
    new_lines = list(lines)
    for a in atoms:
        old = lines[a['line']].split()
        new_line = (f"{old[0]:>7} {old[1]:<4} "
                    f"{a['x']:>10.4f} {a['y']:>10.4f} {a['z']:>10.4f} "
                    + ' '.join(old[5:]) + '\n')
        new_lines[a['line']] = new_line

    with open(mol2_out, 'w') as f:
        f.writelines(new_lines)

    return rmsd

if __name__ == '__main__':
    mol2_in, sdf_orig, pdbqt_docked, mol2_out = sys.argv[1:5]
    rmsd = update_mol2_docked(mol2_in, sdf_orig, pdbqt_docked, mol2_out)
    print(f"OK: post-fit RMSD = {rmsd:.4f} Å")
