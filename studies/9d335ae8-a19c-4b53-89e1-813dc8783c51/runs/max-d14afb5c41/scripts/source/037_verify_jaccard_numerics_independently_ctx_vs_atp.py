
# Verify Jaccard numerics independently
# CTX vs ATP
ctx_cdk2_r  = {54, 57, 58, 121, 122, 123, 151, 152, 153}
atp_main_r  = {15,17,18,30,31,32,33,34,35,46,47,48,49,50,51,52,53,54,55,56,
               58,63,64,65,66,67,76,77,78,79,80,81,82,83,84,85,86,89,
               118,123,125,126,127,128,129,132,134,135,136,137,
               142,143,144,145,146,147,148,149,150,
               158,163,164,165,172,173,175,176,177,178,179,180,185,233,234}

shared_atp  = ctx_cdk2_r & atp_main_r
union_atp   = ctx_cdk2_r | atp_main_r
jaccard_atp = len(shared_atp) / len(union_atp)
print(f"CTX vs ATP — shared: {sorted(shared_atp)}, n={len(shared_atp)}")
print(f"  union: {len(union_atp)}, Jaccard: {jaccard_atp:.4f} (reported 0.04)")

# CTX vs interface
ctx_ccne1_r  = {90,101,102,104,105,107,108,111,149,227,228,229,233,234,237}
iface_cdk2_r = {116,119,120,121,122}
iface_ccne1_r= {90,95,96,97,98,99,100,101,102,103,104,105}
ctx_all      = ctx_cdk2_r | ctx_ccne1_r
iface_all    = iface_cdk2_r | iface_ccne1_r
shared_iface = ctx_all & iface_all
union_iface  = ctx_all | iface_all
jaccard_iface = len(shared_iface) / len(union_iface)
print(f"\nCTX vs Interface — shared: {sorted(shared_iface)}, n={len(shared_iface)}")
print(f"  union: {len(union_iface)}, Jaccard: {jaccard_iface:.4f} (reported 0.21)")

# Verify score formula from code vs report
print("\n--- Score formula verification ---")
# Code:
# v  = 1 if vol<500 else 2 if vol<1500 else 3 if vol<4000 else 4
# h  = 0 if f_hydro<0.25 else 1 if f_hydro<0.40 else 2 if f_hydro<0.50 else 3
# ar = 0 if f_arom<0.05 else 1 if f_arom<0.12 else 2
# raw = v+h+ar+lit;  score = round(raw/12*10, 1)
# Max raw = 4+3+2+3 = 12 → max score = 10. Report says same.
data = [
    ('CRBN main',    2585, 0.42, 0.22, 3),
    ('CRBN zinc',     518, 0.13, 0.00, 0),
    ('CDK2 ATP',     9790, 0.55, 0.09, 3),
    ('CDK2 Tloop',    604, 0.50, 0.19, 1),
    ('Iface apo',     695, 0.47, 0.12, 1),
    ('CTX holo',     2196, 0.58, 0.12, 2),
]
reported = [8.3, 1.7, 9.2, 6.7, 5.8, 8.3]
print(f"{'Pocket':<15} {'computed':>9} {'reported':>9} {'match':>6}")
for (name, vol, hydro, arom, lit), rep in zip(data, reported):
    v  = 1 if vol<500 else (2 if vol<1500 else (3 if vol<4000 else 4))
    h  = 0 if hydro<0.25 else (1 if hydro<0.40 else (2 if hydro<0.50 else 3))
    ar = 0 if arom<0.05 else (1 if arom<0.12 else 2)
    raw = v + h + ar + lit
    score = round(raw/12*10, 1)
    match = "OK" if score == rep else f"MISMATCH (got {score})"
    print(f"  {name:<13} {score:>9.1f} {rep:>9.1f} {match:>6}")
