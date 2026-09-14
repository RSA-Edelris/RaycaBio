
import json

# Pull per-chain self-iptm and cross-chain values for all m0 models
print("=== PER-CHAIN CONFIDENCE (model_0) ===")
print(f"{'Compound':>8}  {'ERα→ERα':>8}  {'CRBN→CRBN':>10}  {'ERα→CRBN':>9}  {'CRBN→ERα':>9}  {'lig→ERα':>8}  {'lig→CRBN':>9}")
print("-"*75)

crbn_self = {}
era_self = {}
for cmpd in [f"ARV_{i:03d}" for i in range(1, 11)]:
    pred = (f"{SESSION}/{cmpd}/boltz_results_{cmpd}_constrained/"
            f"predictions/{cmpd}_constrained")
    with open(f"{pred}/confidence_{cmpd}_constrained_model_0.json") as f:
        d = json.load(f)
    pci = d["pair_chains_iptm"]
    era_s  = pci["0"]["0"]  # ERα → ERα (self)
    crbn_s = pci["1"]["1"]  # CRBN → CRBN (self)
    era_crbn  = pci["0"]["1"]  # ERα → CRBN
    crbn_era  = pci["1"]["0"]  # CRBN → ERα
    lig_era   = pci["2"]["0"]
    lig_crbn  = pci["2"]["1"]
    crbn_self[cmpd] = crbn_s
    era_self[cmpd]  = era_s
    print(f"{cmpd:>8}  {era_s:>8.4f}  {crbn_s:>10.4f}  {era_crbn:>9.4f}  {crbn_era:>9.4f}  {lig_era:>8.4f}  {lig_crbn:>9.4f}")

print()
print(f"Mean ERα self:   {sum(era_self.values())/10:.4f}")
print(f"Mean CRBN self:  {sum(crbn_self.values())/10:.4f}")
print()
print("Note: CRBN→CRBN self-iptm is the model's internal confidence in the CRBN chain")
print("conformation. Values << ERα self indicate CRBN orientation is the dominant")
print("source of uncertainty in these ternary predictions.")
