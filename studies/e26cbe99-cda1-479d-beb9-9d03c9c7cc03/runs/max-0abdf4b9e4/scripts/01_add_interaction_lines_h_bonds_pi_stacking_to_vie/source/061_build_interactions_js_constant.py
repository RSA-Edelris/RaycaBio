
# Build INTERACTIONS JS constant
def js_str(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('`', '\\`')
    s = s.replace('${', '\\${')
    return s

def fmt_vec(v):
    return '{x:' + str(v[0]) + ',y:' + str(v[1]) + ',z:' + str(v[2]) + '}'

lines = ['const INTERACTIONS = {']
for cid, data in interactions.items():
    lines.append(f'  "{cid}": {{')
    lines.append('    "hbonds": [')
    for hb in data['hbonds']:
        label_js = js_str(hb['label'])
        s = fmt_vec(hb['start'])
        e = fmt_vec(hb['end'])
        lines.append(f'      {{start:{s}, end:{e}, label:"{label_js}"}},')
    lines.append('    ],')
    lines.append('    "pistack": [')
    for ps in data['pistack']:
        label_js = js_str(ps['label'])
        s = fmt_vec(ps['start'])
        e = fmt_vec(ps['end'])
        lines.append(f'      {{start:{s}, end:{e}, label:"{label_js}"}},')
    lines.append('    ]')
    lines.append('  },')
lines.append('};')

interactions_js = '\n'.join(lines)
print(interactions_js[:600])
print('...')
print(f'\nTotal length: {len(interactions_js)} chars')
