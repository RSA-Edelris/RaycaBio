
import json

def extract_all_routes(r):
    """Extract route list with full reaction/leaf details from AiZynthFinder output."""
    routes = []
    raw_routes = r.get("output", {}).get("routes", r.get("routes", []))
    
    def walk(node, path=None):
        """Return list of (product_smiles, reaction_smiles, reactants) tuples, top-down."""
        if path is None:
            path = []
        if not isinstance(node, dict):
            return []
        steps = []
        children = node.get("children", [])
        for child in children:
            if child.get("type") == "reaction":
                rxn_smiles = child.get("smiles", "")
                meta = child.get("metadata", {})
                template = meta.get("template", "")
                classification = meta.get("classification", "")
                library_occ = meta.get("library_occurence", 0)
                prob = meta.get("policy_probability", 0)
                # get products of this reaction (the node above)
                product = node.get("smiles", "")
                # get reactants
                reactants = [c.get("smiles","") for c in child.get("children",[]) if c.get("type")=="mol"]
                steps.append({
                    "product": product,
                    "rxn_smiles": rxn_smiles,
                    "reactants": reactants,
                    "template": template,
                    "classification": classification,
                    "library_occ": library_occ,
                    "policy_prob": prob,
                })
                # recurse into reactants that are not in stock
                for c in child.get("children", []):
                    if c.get("type") == "mol" and not c.get("in_stock", True):
                        steps.extend(walk(c))
        return steps

    for route in raw_routes:
        rt = route.get("reaction_tree", route)
        steps = walk(rt)
        leaves = []
        def get_leaves(node):
            if not isinstance(node, dict): return
            ch = node.get("children", [])
            if not ch and node.get("type") == "mol":
                leaves.append({"smiles": node.get("smiles",""), "in_stock": node.get("in_stock", False)})
                return
            for c in ch:
                if c.get("type") == "reaction":
                    for gc in c.get("children", []):
                        if gc.get("type") == "mol":
                            if not gc.get("children"):
                                leaves.append({"smiles": gc.get("smiles",""), "in_stock": gc.get("in_stock",False)})
                            else:
                                get_leaves(gc)
        get_leaves(rt)
        routes.append({
            "rank": route.get("rank"),
            "is_solved": route.get("is_solved"),
            "depth": route.get("depth"),
            "n_reactions": route.get("n_reactions"),
            "score": route.get("scores", {}).get("state score", None),
            "steps": steps,
            "leaves": leaves,
        })
    return routes

for name in ["MCUF651", "A317", "7977"]:
    r = aizyn_results[name]
    routes = extract_all_routes(r)
    print(f"\n{'='*70}")
    print(f"TARGET: {name}  |  solved={r['output']['is_solved']}  |  n_routes={r['output']['n_routes']}  |  n_solved={r['output']['n_solved_routes']}")
    for route in routes:
        print(f"\n  Route {route['rank']}  score={route['score']:.4f}  steps={route['n_reactions']}  solved={route['is_solved']}")
        for i, step in enumerate(route['steps'], 1):
            print(f"    Step {i}: {' + '.join(step['reactants'])} -> {step['product']}")
            print(f"           lib_occ={step['library_occ']}  prob={step['policy_prob']:.4f}  class={step['classification']}")
        print(f"    SMs: {[l['smiles'] for l in route['leaves']]}")
