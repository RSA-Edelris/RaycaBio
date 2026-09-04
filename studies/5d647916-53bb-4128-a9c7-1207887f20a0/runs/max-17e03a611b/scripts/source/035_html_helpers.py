
import html as H

# ── HTML helpers ─────────────────────────────────────────────────────────────
def mol_box_html(smiles, name, role):
    b64 = SVG_CACHE.get(smiles, '')
    cls = {'sm': 'mol-sm', 'int': 'mol-int', 'prod': 'mol-prod'}.get(role, 'mol-int')
    tag = {'sm': 'SM', 'int': 'INT', 'prod': '★ TARGET'}.get(role, '')
    if b64:
        img = f'<img class="mol-img" src="data:image/svg+xml;base64,{b64}" width="175" height="125" alt="{H.escape(smiles)}">'
    else:
        img = f'<div class="mol-err">{H.escape(smiles[:30])}</div>'
    name_lines = name.replace('\n', '<br>')
    return (f'<div class="mol-box {cls}">'
            f'<span class="mol-role-tag tag-{role}">{tag}</span>'
            f'<div class="mol-img-wrap">{img}</div>'
            f'<div class="mol-name">{name_lines}</div>'
            f'</div>')

def arrow_html(reagents, conditions, yld):
    reag_html = '<br>'.join(H.escape(r) for r in reagents)
    cond_html = H.escape(conditions).replace('\n', '<br>')
    return (f'<div class="arrow-block">'
            f'<div class="arrow-reagents">{reag_html}</div>'
            f'<div class="arrow-shaft"><div class="arrow-line"></div>'
            f'<div class="arrow-head">▶</div></div>'
            f'<div class="arrow-conditions">{cond_html}</div>'
            f'<div class="arrow-yield">{H.escape(yld)}</div>'
            f'</div>')

def scheme_html(steps):
    parts = []
    for s in steps:
        if s[0] == 'mol':
            _, smi, name, role = s
            parts.append(mol_box_html(smi, name, role))
        elif s[0] == 'arrow':
            _, reagents, conditions, yld = s
            parts.append(arrow_html(reagents, conditions, yld))
    return f'<div class="scheme-row">{"".join(parts)}</div>'

def route_html(route):
    lbl = H.escape(route['label'])
    tag = H.escape(route['tag'])
    strat = H.escape(route['strategic'])
    scheme = scheme_html(route['steps'])
    # count steps (number of arrows)
    n_steps = sum(1 for s in route['steps'] if s[0] == 'arrow')
    return (f'<div class="route-block">'
            f'<div class="route-header">'
            f'<span class="route-label">{lbl}</span>'
            f'<span class="route-tag">{tag}</span>'
            f'<span class="route-steps">{n_steps} step{"s" if n_steps>1 else ""}</span>'
            f'</div>'
            f'<div class="route-strategic">Key disconnection: {strat}</div>'
            f'{scheme}'
            f'</div>')

def compound_section_html(cpd):
    cid = H.escape(cpd['id'])
    fname = H.escape(cpd['full_name'])
    tgt_b64 = SVG_CACHE.get(cpd['target_smiles'], '')
    tgt_img = (f'<img class="tgt-thumb" src="data:image/svg+xml;base64,{tgt_b64}" '
               f'width="200" height="140" alt="target">') if tgt_b64 else ''
    routes_html = ''.join(route_html(r) for r in cpd['routes'])
    n_routes = len(cpd['routes'])
    return (f'<section class="compound-section" id="{cid}">'
            f'<div class="compound-header">'
            f'<div class="compound-title-block">'
            f'<h2 class="compound-name">{fname}</h2>'
            f'<span class="compound-meta">{n_routes} route{"s" if n_routes>1 else ""} shown</span>'
            f'</div>'
            f'<div class="compound-thumb-wrap">{tgt_img}</div>'
            f'</div>'
            f'{routes_html}'
            f'</section>')

print("HTML builder functions defined. Building full page…")
