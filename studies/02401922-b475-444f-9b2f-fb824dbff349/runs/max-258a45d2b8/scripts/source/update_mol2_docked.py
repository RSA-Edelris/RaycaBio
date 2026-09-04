#!/usr/bin/env python3
"""
Rigid-body superpose antechamber mol2 onto Vina docked PDBQT (first pose).
PDBQT heavy atom order matches mol2 heavy atom order (both from same SDF).
Updates all 73 mol2 atom coordinates; preserves GAFF2 types + AM1-BCC charges.
"""
import sys, re
import numpy as np

def parse_mol2_atoms(path):
    """Return list of (line_idx, atom_name, x, y, z, rest, is_H)."""
    lines = open(path).readlines()
    in_atom = False
    atoms = []
    indices = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '@<TRIPOS>ATOM':
            in_atom = True
            continue
        if in_atom and stripped.startswith('@'):
            in_atom = False
        if in_atom and stripped:
            parts = line.split()
            if len(parts) >= 6:
                atom_type = parts[5].lower()
                is_h = atom_type.startswith('h')
                try:
                    x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
                    atoms.append({'line': i, 'name': parts[1], 'x': x, 'y': y, 'z': z,
                                  'type': parts[5], 'rest': parts[6:], 'is_h': is_h})
                    indices.append(i)
                except ValueError:
                    pass
    return lines, atoms

def parse_pdbqt_first_pose_heavy(path):
    """Return Nx3 array of heavy atom positions from first MODEL."""
    coords = []
    in_first = False
    seen_model = False
    for line in open(path):
        if line.startswith('MODEL'):
            if seen_model:
                break
            seen_model = True
            in_first = True
            continue
        if line.startswith('ENDMDL'):
            break
        if in_first and (line.startswith('ATOM') or line.startswith('HETATM')):
            ad_type = line[77:79].strip()  # AutoDock atom type in last cols
            if ad_type == 'HD':
                continue  # skip polar H
            try:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                coords.append([x, y, z])
            except ValueError:
                pass
    return np.array(coords)

def rigid_superpose(ref_pts, mob_pts):
    """SVD rigid body fit: returns R, t such that R @ mob_pts[i] + t ≈ ref_pts[i]."""
    assert len(ref_pts) == len(mob_pts), f"atom count mismatch: {len(ref_pts)} vs {len(mob_pts)}"
    c_ref = ref_pts.mean(axis=0)
    c_mob = mob_pts.mean(axis=0)
    A = (ref_pts - c_ref).T @ (mob_pts - c_mob)
    U, S, Vt = np.linalg.svd(A)
    d = np.linalg.det(U @ Vt)
    D = np.diag([1, 1, d])
    R = U @ D @ Vt
    t = c_ref - R @ c_mob
    return R, t

def update_mol2(mol2_in, pdbqt_in, mol2_out):
    lines, atoms = parse_mol2_atoms(mol2_in)
    heavy_atoms = [a for a in atoms if not a['is_h']]
    pdbqt_heavy = parse_pdbqt_first_pose_heavy(pdbqt_in)

    if len(heavy_atoms) != len(pdbqt_heavy):
        raise ValueError(f"Heavy atom mismatch: mol2={len(heavy_atoms)}, pdbqt={len(pdbqt_heavy)}")

    mob = np.array([[a['x'], a['y'], a['z']] for a in heavy_atoms])
    R, t = rigid_superpose(pdbqt_heavy, mob)

    # Apply R, t to all atoms
    for a in atoms:
        orig = np.array([a['x'], a['y'], a['z']])
        new = R @ orig + t
        a['x'], a['y'], a['z'] = new

    # Rewrite mol2 with updated coordinates
    new_lines = list(lines)
    for a in atoms:
        i = a['line']
        old = lines[i].split()
        # mol2 atom line: id name x y z type [subst_id subst_name charge]
        new_line = (f"{old[0]:>7} {old[1]:<4} "
                    f"{a['x']:>10.4f} {a['y']:>10.4f} {a['z']:>10.4f} "
                    + ' '.join(old[5:]) + '\n')
        new_lines[i] = new_line

    with open(mol2_out, 'w') as f:
        f.writelines(new_lines)

    rmsd = np.sqrt(np.mean(np.sum((pdbqt_heavy - np.array([[a['x'],a['y'],a['z']] for a in atoms if not a['is_h']]))**2, axis=1)))
    return len(heavy_atoms), rmsd

if __name__ == '__main__':
    mol2_in, pdbqt_in, mol2_out = sys.argv[1], sys.argv[2], sys.argv[3]
    n, rmsd = update_mol2(mol2_in, pdbqt_in, mol2_out)
    print(f"OK: {n} heavy atoms mapped, post-fit RMSD={rmsd:.3f} Å")
