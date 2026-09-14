
import json, os
import numpy as np

SESSION = "/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74"

results = {}
for cmpd in [f"ARV_{i:03d}" for i in range(1, 11)]:
    pred_dir = f"{SESSION}/{cmpd}/boltz_results_{cmpd}_constrained/predictions/{cmpd}_constrained"
    results[cmpd] = {}
    for m in range(3):
        jf = f"{pred_dir}/confidence_{cmpd}_constrained_model_{m}.json"
        with open(jf) as f:
            d = json.load(f)
        pci = d.get("pair_chains_iptm", {})
        # Chain indexing: "0"=ERα, "1"=CRBN, "2"=ligand
        lig_erα  = pci.get("2", {}).get("0", None)
        lig_crbn = pci.get("2", {}).get("1", None)
        results[cmpd][m] = {
            "conf":      d.get("confidence_score", d.get("confidence", None)),
            "iptm":      d.get("iptm", None),
            "lig_iptm":  d.get("ligand_iptm", None),
            "lig_erα":   lig_erα,
            "lig_crbn":  lig_crbn,
            "prot_iptm": d.get("prot_iptm", None),
            "pci_keys":  {k: list(v.keys()) for k, v in pci.items()},
        }
        print(f"{cmpd} m{m}: conf={results[cmpd][m]['conf']:.4f}  lig_crbn={lig_crbn}  lig_erα={lig_erα}  pci={results[cmpd][m]['pci_keys']}")
