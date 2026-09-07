
# Fix: SDF property tag uses "> <field>" (one space), not ">  <field>"
pose_table = []
for i, blk in enumerate(blocks):
    lines = blk.splitlines()
    mol_name = lines[0].strip()
    props = {}
    for j, ln in enumerate(lines):
        m = re.match(r'> {1,2}<(.+?)>', ln)   # 1 or 2 spaces
        if m:
            key = m.group(1)
            val = lines[j+1].strip() if j+1 < len(lines) else ''
            props[key] = val

    def fget(k): 
        try: return float(props[k])
        except: return float('nan')

    aff       = fget('minimizedAffinity')
    cnn_score = fget('CNNscore')
    cnn_aff   = fget('CNNaffinity')
    cnn_vs    = fget('CNN_VS')
    pic50     = props.get('pIC50 PDK', '')

    same = [p for p in pose_table if p['mol_name'] == mol_name]
    rank = len(same) + 1

    pose_table.append({
        'global_idx': i+1, 'mol_name': mol_name, 'rank': rank,
        'affinity': aff, 'cnn_score': cnn_score,
        'cnn_aff': cnn_aff, 'cnn_vs': cnn_vs,
        'pic50': pic50, 'block': blk, 'props': props
    })

print(f"{'Molecule':22s}  {'Rank':>4}  {'Affinity':>10}  {'CNNscore':>10}  {'CNNaff':>9}  {'pIC50':>6}")
print("-"*75)
for r in pose_table:
    aff_s = f"{r['affinity']:10.4f}" if r['affinity'] == r['affinity'] else "       nan"
    cnn_s = f"{r['cnn_score']:10.4f}" if r['cnn_score'] == r['cnn_score'] else "       nan"
    caf_s = f"{r['cnn_aff']:9.4f}"  if r['cnn_aff'] == r['cnn_aff']   else "      nan"
    print(f"{r['mol_name']:22s}  {r['rank']:>4}  {aff_s}  {cnn_s}  {caf_s}  {r['pic50']:>6}")
