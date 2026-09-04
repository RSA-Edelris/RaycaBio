
import json

# Extract a compact summary of routes without dumping the whole tree
def summarise_routes(r):
    out = {}
    for k, v in r.items():
        if k == "routes":
            routes_summary = []
            for i, route in enumerate(v[:10] if isinstance(v, list) else []):
                if not isinstance(route, dict):
                    continue
                # Try common key names
                score = route.get("score", route.get("state_score", route.get("total_score", "?")))
                is_solved = route.get("is_solved", route.get("solved", "?"))
                # Count steps by walking the tree
                def count_reactions(node, depth=0):
                    if not isinstance(node, dict):
                        return 0
                    children = node.get("children", [])
                    n = 1 if node.get("type") == "reaction" else 0
                    for c in children:
                        n += count_reactions(c, depth+1)
                    return n
                n_rxn = count_reactions(route)
                # Get leaf SMILES (starting materials)
                def get_leaves(node):
                    if not isinstance(node, dict):
                        return []
                    children = node.get("children", [])
                    if not children and node.get("type") == "mol":
                        return [node.get("smiles","?")]
                    leaves = []
                    for c in children:
                        leaves.extend(get_leaves(c))
                    return leaves
                leaves = get_leaves(route)
                # Get reaction SMILES
                def get_reactions(node):
                    if not isinstance(node, dict):
                        return []
                    rxns = []
                    if node.get("type") == "reaction":
                        rxns.append(node.get("smiles", node.get("reaction_smiles", "?")))
                    for c in node.get("children", []):
                        rxns.extend(get_reactions(c))
                    return rxns
                rxns = get_reactions(route)
                routes_summary.append({
                    "route_idx": i,
                    "score": score,
                    "is_solved": is_solved,
                    "n_reactions": n_rxn,
                    "reactions": rxns,
                    "starting_materials": leaves,
                })
            out["routes"] = routes_summary
        elif k not in ("summary",):
            out[k] = v
    return out

for name in ["MCUF651", "A317", "7977"]:
    r = aizyn_results[name]
    compact = summarise_routes(r)
    print(f"\n{'='*60}\nTARGET: {name}")
    print(json.dumps(compact, indent=2)[:6000])
