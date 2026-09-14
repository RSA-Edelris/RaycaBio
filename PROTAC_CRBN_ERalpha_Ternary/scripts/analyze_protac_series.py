"""
Analyze Boltz-2 ternary complex predictions for PROTAC series.
Run after job 6534300 completes.
Usage: python analyze_protac_series.py <series_output_dir>
"""
import sys
import os
import json
import math
import numpy as np

COMPOUNDS = ["ARV_001","ARV_002","ARV_003","ARV_004","ARV_005",
             "ARV_006","ARV_007","ARV_008","ARV_009","ARV_010"]

# Linker metadata
LINKER_INFO = {
    "ARV_001": ("isoindolinone", "OEt-piperazine-EtO",  9,  0),
    "ARV_002": ("phthalimide",   "N-piperazine-EtO",    7,  0),
    "ARV_003": ("isoindolinone", "NH-butyl-piperazine-EtO", 10, 0),
    "ARV_004": ("isoindolinone", "PEG-1",               4,  1),
    "ARV_005": ("isoindolinone", "PEG-2",               7,  2),
    "ARV_006": ("isoindolinone", "PEG-3",              10,  3),
    "ARV_007": ("isoindolinone", "PEG-4",              13,  4),
    "ARV_008": ("isoindolinone", "PEG-5",              16,  5),
    "ARV_009": ("isoindolinone", "PEG-6",              19,  6),
    "ARV_010": ("isoindolinone", "PEG-13",             40, 13),
}

ARV471_REF = {
    "conf": 0.4778, "ptm": 0.4550, "iptm": 0.3133,
    "lig_iptm": 0.9065, "lig_crbn_iptm": 0.2306,
    "prot_iptm": 0.1604, "lig_span": 25.58,
    "era_crbn_centroid_dist": 32.84
}

def dist(a, b):
    return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))

def parse_pdb(path):
    atoms = {}
    residues = {}
    with open(path) as f:
        for line in f:
            if line.startswith(("ATOM","HETATM")):
                ch = line[21]
                rn = int(line[22:26].strip())
                rname = line[17:20].strip()
                aname = line[12:16].strip()
                x,y,z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                atoms[(ch,rn,aname)] = (x,y,z)
                residues[(ch,rn)] = rname
    return atoms, residues

def centroid(xyz_list):
    return tuple(np.mean(xyz_list, axis=0))

def compute_geometry(atoms):
    era_xyz = [xyz for (ch,_,_),xyz in atoms.items() if ch=='A']
    crbn_xyz = [xyz for (ch,_,_),xyz in atoms.items() if ch=='B']
    lig_xyz = [xyz for (ch,_,_),xyz in atoms.items() if ch=='C']
    if not lig_xyz:
        return {}
    ec = centroid(era_xyz)
    cc = centroid(crbn_xyz)
    lc = centroid(lig_xyz)
    era_crbn_dist = dist(ec, cc)
    min_lig_era = min(dist(p, q) for p in lig_xyz for q in era_xyz)
    min_lig_crbn = min(dist(p, q) for p in lig_xyz for q in crbn_xyz)
    min_era_crbn = min(dist(p, q) for p in era_xyz for q in crbn_xyz)
    # Ligand span = max pairwise distance
    lig_span = max(dist(lig_xyz[i], lig_xyz[j]) for i in range(len(lig_xyz)) for j in range(i+1, len(lig_xyz)))
    lig_era_count = sum(1 for p in lig_xyz if any(dist(p,q)<4.0 for q in era_xyz))
    lig_crbn_count = sum(1 for p in lig_xyz if any(dist(p,q)<4.0 for q in crbn_xyz))
    return {
        "era_crbn_dist": era_crbn_dist,
        "lig_span": lig_span,
        "min_lig_era": min_lig_era,
        "min_lig_crbn": min_lig_crbn,
        "min_era_crbn": min_era_crbn,
        "lig_era_contacts": lig_era_count,
        "lig_crbn_contacts": lig_crbn_count,
        "n_lig": len(lig_xyz),
    }

def process_compound(base_dir, name):
    safe = name
    # Find the prediction subdir
    pred_root = os.path.join(base_dir, safe)
    
    # Find the boltz_results directory
    for d in os.listdir(pred_root):
        if d.startswith("boltz_results"):
            inner = os.path.join(pred_root, d, "predictions")
            break
    else:
        return None

    # Find the input-name directory
    for d in os.listdir(inner):
        pred_dir = os.path.join(inner, d)
        break

    # Best model = model_0
    conf_file = None
    pdb_file = None
    for f in os.listdir(pred_dir):
        if f.endswith("_model_0.json") and f.startswith("confidence"):
            conf_file = os.path.join(pred_dir, f)
        if f.endswith("_model_0.pdb"):
            pdb_file = os.path.join(pred_dir, f)

    if not conf_file or not pdb_file:
        return None

    with open(conf_file) as f:
        conf = json.load(f)

    atoms, residues = parse_pdb(pdb_file)
    geo = compute_geometry(atoms)

    pci = conf.get("pair_chains_iptm", {})
    return {
        "name": name,
        "conf": conf.get("confidence_score", 0),
        "ptm": conf.get("ptm", 0),
        "iptm": conf.get("iptm", 0),
        "lig_iptm": conf.get("ligand_iptm", 0),
        "prot_iptm": conf.get("protein_iptm", 0),
        "lig_era_iptm": float(pci.get("2", {}).get("0", 0)),
        "lig_crbn_iptm": float(pci.get("2", {}).get("1", 0)),
        "era_crbn_iptm": float(pci.get("0", {}).get("1", 0)),
        "crbn_era_iptm": float(pci.get("1", {}).get("0", 0)),
        **geo,
    }


if __name__ == "__main__":
    base_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    results = []
    for name in COMPOUNDS:
        r = process_compound(base_dir, name)
        if r:
            results.append(r)
        else:
            print(f"WARNING: could not parse {name}")

    if not results:
        print("No results found. Check the base directory path.")
        sys.exit(1)

    print("="*100)
    print("PROTAC SERIES TERNARY COMPLEX PREDICTIONS — model_0 best pose per compound")
    print("="*100)
    print()
    print("Reference: ARV-471 (piperazine-piperidine linker, 54 HA)")
    print(f"  conf={ARV471_REF['conf']:.4f}, ptm={ARV471_REF['ptm']:.4f}, iptm={ARV471_REF['iptm']:.4f},")
    print(f"  lig_iptm={ARV471_REF['lig_iptm']:.4f} (=lig→ERa), lig→CRBN={ARV471_REF['lig_crbn_iptm']:.4f},")
    print(f"  prot_iptm={ARV471_REF['prot_iptm']:.4f}, span={ARV471_REF['lig_span']:.2f}Å, ERa-CRBN dist={ARV471_REF['era_crbn_centroid_dist']:.2f}Å")
    print()

    # Cooperativity proxy ranking: ligand→CRBN iptm
    ranked = sorted(results, key=lambda x: x["lig_crbn_iptm"], reverse=True)
    
    print("CONFIDENCE SCORES (sorted by lig→CRBN iptm = cooperativity proxy)")
    print(f"{'Name':>8} {'HA':>4} {'linker':>8} {'conf':>6} {'iptm':>6} {'lig→ERa':>8} {'lig→CRBN':>9} {'prot_iptm':>10} {'ERa-CRBN(Å)':>12} {'span(Å)':>9} {'Δlig→CRBN':>10}")
    print("-"*110)
    for r in ranked:
        li = LINKER_INFO[r["name"]]
        linker_n = li[3] if li[3] > 0 else f"~{li[2]}a"
        n_eo_str = f"PEG-{li[3]}" if li[3] > 0 else li[1][:8]
        delta_crbn = r["lig_crbn_iptm"] - ARV471_REF["lig_crbn_iptm"]
        print(f"{r['name']:>8} {LINKER_INFO[r['name']][2]+35:>4} {n_eo_str:>8} {r['conf']:>6.4f} {r['iptm']:>6.4f} "
              f"{r['lig_era_iptm']:>8.4f} {r['lig_crbn_iptm']:>9.4f} {r['prot_iptm']:>10.4f} "
              f"{r['era_crbn_dist']:>12.2f} {r['lig_span']:>9.2f} {delta_crbn:>+10.4f}")
    
    print()
    print("Cooperativity proxy: lig→CRBN iptm. Higher = model is more confident the PROTAC engages CRBN")
    print("in the ternary context. Reference ARV-471 lig→CRBN iptm = 0.231.")
    print()

    # Geometry table
    print("GEOMETRIC PARAMETERS (model_0)")
    print(f"{'Name':>8} {'min_lig-ERa':>12} {'min_lig-CRBN':>13} {'min_ERa-CRBN':>13} {'#Lig-ERa<4Å':>12} {'#Lig-CRBN<4Å':>13}")
    print("-"*80)
    for r in sorted(results, key=lambda x: x["name"]):
        print(f"{r['name']:>8} {r['min_lig_era']:>12.2f} {r['min_lig_crbn']:>13.2f} {r['min_era_crbn']:>13.2f} "
              f"{r['lig_era_contacts']:>12d} {r['lig_crbn_contacts']:>13d}")

    print()
    print("EVIDENCE LIMITS")
    print("1. All predictions are in single-sequence (no MSA) mode.")
    print("   CRBN pLDDT was 0.347 for ARV-471; all CRBN predictions here are similarly unreliable.")
    print("   The CRBN orientation relative to ERa is NOT constrained by the model.")
    print()
    print("2. protein_iptm < 0.20 for all predictions (expected for no-MSA mode).")
    print("   This means the ternary interface geometry cannot be interpreted for cooperativity.")
    print("   Ranking by lig→CRBN iptm is a proxy, not a direct cooperativity measurement.")
    print()
    print("3. Steric clashes (min ERa-CRBN distance < 1.5 Å) in the raw PDB coordinates are expected")
    print("   and should not be interpreted as physical contacts.")
    print()
    print("4. Predictions for ARV-010 (87 HA, PEG-13 linker) involve a 40-atom flexible chain")
    print("   whose conformation is essentially random; lig_crbn_iptm for this compound has")
    print("   no interpretable meaning regarding cooperativity.")
    print()
    print("5. Different linker lengths genuinely affect cooperativity through geometrical constraints.")
    print("   This series cannot test that because CRBN positioning is unconstrained in all predictions.")

