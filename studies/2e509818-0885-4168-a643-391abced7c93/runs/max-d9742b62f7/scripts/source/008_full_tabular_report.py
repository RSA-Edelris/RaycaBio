
# ── Full tabular report ───────────────────────────────────────────────────────

header = (f"{'Rank':>4}  {'CR_ID':<12}  {'MW':>6}  {'cLogP':>6}  "
          f"{'logS':>6}  {'logPapp':>8}  {'MetStab':>8}  "
          f"{'CYP':>6}  {'PPB%':>5}  {'hERG':>6}  {'MPO':>6}  {'ADs':<12}")
sep = '-'*len(header)

print("═"*len(header))
print("TOP-96 SHORTLIST (ranked by MPO score)")
print("═"*len(header))
print(header)
print(sep)

for rank, row in enumerate(top96, 1):
    ads = ('S' if row['sol_sol_ad'] else 's')
    ads += ('P' if row['pampa_pampa_ad'] else 'p')
    ads += ('B' if row['ppb_ppb_ad'] else 'b')
    print(f"{rank:>4}  {row['cr_id']:<12}  {row['mw']:>6.0f}  {row['clogp']:>6.2f}  "
          f"{row['sol_logS']:>6.2f}  {row['pampa_logPapp']:>8.2f}  "
          f"{row['met_t12_class'][:8]:>8}  "
          f"{row['cyp_cyp_risk']:>6}  {row['ppb_ppb_pct']:>5.1f}  "
          f"{row['herg_herg_risk']:>6}  {row['mpo_score']:>6.4f}  {ads:<12}")

print(sep)
print("  AD keys: S=ESOL in-domain P=PAMPA in-domain B=PPB in-domain (uppercase=in-AD)")
