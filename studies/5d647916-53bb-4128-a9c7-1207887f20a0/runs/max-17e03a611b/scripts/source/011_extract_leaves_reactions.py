
import json

def extract_leaves_and_reactions(node, leaves=None, reactions=None, depth=0):
    if leaves is None: leaves = []
    if reactions is None: reactions = []
    t = node.get("type", "")
    if t == "mol":
        if not node.get("children"):
            leaves.append({"smiles": node["smiles"], "in_stock": node.get("in_stock", False)})
    elif t == "reaction":
        meta = node.get("metadata", {})
        reactions.append({
            "depth": depth,
            "classification": meta.get("classification", "?"),
            "library_occurence": meta.get("library_occurence", 0),
            "policy_probability": meta.get("policy_probability", 0),
            "template": meta.get("template", ""),
            "mapped_rxn": meta.get("mapped_reaction_smiles", "")[:200],
        })
    for child in node.get("children", []):
        extract_leaves_and_reactions(child, leaves, reactions, depth + 1)
    return leaves, reactions

target_files = {
    "MCUF651": ("aizynthfinder-results.json",   "CN(C)CCN1CCC[C@H](C(=O)Nc2nc3c(F)cc(F)cc3s2)C1"),
    "A317":    ("aizynthfinder-results-2.json",  "O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1"),
    "8008":    ("aizynthfinder-results-3.json",  "CCOc1ccc(S(=O)(=O)Nc2ccc(Cl)cc2C#Cc2cnc(C(=O)O)cc2OC)c2ncccc12"),
    "7977":    ("aizynthfinder-results-4.json",  "Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21"),
    "7877":    ("aizynthfinder-results-5.json",  "Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)O)c(C5CCCC5)c4)c3c2)c1"),
}

all_parsed = {}
for name, (fname, target_smi) in target_files.items():
    with open(fname) as fh:
        raw = json.load(fh)
    # raw is the direct output (not wrapped)
    routes = raw.get("routes", [])
    parsed_routes = []
    for r in routes:
        tree = r.get("reaction_tree", {})
        leaves, reactions = extract_leaves_and_reactions(tree)
        parsed_routes.append({
            "rank": r["rank"],
            "is_solved": r["is_solved"],
            "depth": r["depth"],
            "n_reactions": r["n_reactions"],
            "n_leaves": r["n_leaves"],
            "n_leaves_in_stock": r["n_leaves_in_stock"],
            "leaves": leaves,
            "reactions": reactions,
            "tree_json": tree,
        })
    all_parsed[name] = {
        "target": target_smi,
        "is_solved": raw.get("is_solved"),
        "top_score": raw.get("top_score"),
        "routes": parsed_routes,
    }
    print(f"\n{name}: solved={raw.get('is_solved')} top_score={raw.get('top_score'):.4f}")
    for pr in parsed_routes:
        leaves_str = ", ".join(
            f"{l['smiles']}{'*' if l['in_stock'] else ''}" for l in pr["leaves"]
        )
        rxn_classes = [rx["classification"] for rx in pr["reactions"]]
        print(f"  Route {pr['rank']}: solved={pr['is_solved']} depth={pr['depth']} "
              f"n_rxns={pr['n_reactions']} stock={pr['n_leaves_in_stock']}/{pr['n_leaves']}")
        print(f"    Reactions: {rxn_classes}")
        print(f"    Leaves: {leaves_str}")

with open("all_parsed_routes.json", "w") as fh:
    json.dump(all_parsed, fh, indent=2)
print("\nSaved to all_parsed_routes.json")
