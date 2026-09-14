
import json, os

SESSION = "/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74"

scores_by_compound = {}
for i in range(1, 11):
    cmpd = f"ARV_{i:03d}"
    pred = f"{SESSION}/{cmpd}/boltz_results_{cmpd}_constrained/predictions/{cmpd}_constrained"
    models = []
    for m in range(3):
        jf = f"{pred}/confidence_{cmpd}_constrained_model_{m}.json"
        with open(jf) as f:
            d = json.load(f)
        pci = d["pair_chains_iptm"]
        models.append({
            "model": m,
            "conf": round(d["confidence_score"], 4),
            "ptm": round(d["ptm"], 4),
            "iptm": round(d["iptm"], 4),
            "ligand_iptm": round(d.get("ligand_iptm", 0), 4),
            "protein_iptm": round(d.get("protein_iptm", 0), 4),
            "complex_plddt": round(d.get("complex_plddt", 0), 4),
            "era_self": round(float(pci["0"]["0"]), 4),
            "crbn_self": round(float(pci["1"]["1"]), 4),
            "era_crbn": round(float(pci["0"]["1"]), 4),
            "crbn_era": round(float(pci["1"]["0"]), 4),
            "lig_era": round(float(pci["2"]["0"]), 4),
            "lig_crbn": round(float(pci["2"]["1"]), 4),
        })
    scores_by_compound[cmpd] = models

# Best model per compound by lig_crbn
best = {c: max(ms, key=lambda x: x["lig_crbn"]) for c, ms in scores_by_compound.items()}
ranked = sorted(best.items(), key=lambda x: -x[1]["lig_crbn"])

# unconstrained reference values (from job 6534300, hardcoded from prior run)
unconstrained = {
    "ARV_001": 0.5086, "ARV_002": 0.2718, "ARV_003": 0.4059,
    "ARV_004": 0.2657, "ARV_005": 0.3461, "ARV_006": 0.4331,
    "ARV_007": 0.1932, "ARV_008": 0.3331, "ARV_009": 0.3574,
    "ARV_010": 0.2454,
}

# Surface lysine data (3.5-12 Å, from prior analysis)
surface_lys = {
    "ARV_001": [("K235",3.5),("K176",5.7),("K153",6.6),("K3",8.0),("K7",8.0),("K224",9.8),("K6",10.5)],
    "ARV_002": [("K224",4.6),("K153",8.2),("K7",8.3),("K233",8.4),("K3",9.4),("K235",10.0),("K171",10.5),("K185",11.2)],
    "ARV_003": [("K233",6.7),("K153",11.3),("K235",11.4),("K7",11.9)],
    "ARV_004": [("K224",4.1),("K233",5.6),("K7",5.7),("K171",6.1),("K153",8.1),("K185",8.2),("K3",8.5),("K235",10.5),("K120",11.0),("K6",11.5)],
    "ARV_005": [("K233",5.0),("K171",5.7),("K224",6.2),("K105",6.8),("K7",7.4),("K235",8.0),("K153",8.7),("K176",8.9),("K185",10.2),("K3",11.2)],
    "ARV_006": [("K171",3.7),("K176",3.8),("K120",5.2),("K3",6.4),("K105",8.5),("K6",10.4),("K196",10.4),("K235",10.4)],
    "ARV_007": [("K105",3.9),("K171",4.1),("K176",5.4),("K224",5.8),("K235",6.3),("K3",7.8),("K120",8.8),("K185",9.9),("K6",10.5),("K153",10.8)],
    "ARV_008": [("K7",3.7),("K171",5.1),("K233",7.3),("K176",9.1),("K153",9.3),("K185",9.9)],
    "ARV_009": [("K233",3.9),("K66",4.4),("K153",5.6),("K171",6.7),("K7",8.4),("K6",8.9),("K196",11.0)],
    "ARV_010": [("K224",3.8),("K7",4.0),("K153",5.6),("K171",6.5),("K105",6.8),("K3",6.9),("K176",8.4),("K233",8.5),("K196",8.9),("K185",9.3),("K6",9.9),("K235",9.9),("K120",11.3)],
}

print("Data ready. Building documents...")
print(f"Ranked (best model): {[(c, b['lig_crbn'], f'm{b[\"model\"]}') for c,b in ranked]}")
